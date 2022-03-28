from pathlib import Path
import shanoir_downloader
import sys
import zipfile
import os
import glob
from datetime import datetime

#
# Script to download and BIDS-like organize data on Shanoir using "shanoir_downloader.py" developed by Arthur Masson
# @Author: Malo Gaubert < malo.gaubert@irisa.fr >
# @Date: November 2021
# @Update: March 2022: download archive with DICOM files in it and organize the data following BIDS-like structure (no DICOM extraction, only zip file are renamed)
#
# First, you need to adapt the script to your purpose, notably:
#   - dataOrganization, dictionary containing the name of each sequence on Shanoir, their BIDS subdirectory (under sub-????) and their bids filename
#   - studyIDSearch: the name of the database on Shanoir
#   - subjectToSearch: the ID of the subject to search; put a star (*) for all subjects
#   - idSeq: list of the ID of the sequences in dataOrganization
#   - pathOutputDir: path where the BIDS-like database will be created
#   - shanoirID: your ID on Shanoir (usually, your INRIA ID)
#   - filetype: filetype of the data to download: either NIFTI (conversion done by Shanoir using dcm2niix) or DICOM
#
# Then, you can launch directly in a console using "python ./download_all_data.py"
#
# Of note, you will need to enter your Shanoir password.
# 


##############################################################################################
# TO ADAPT
##############################################################################################
# Dictionary of dictionary for data organization composed, for each line:
#   - datasetName: Name on Shanoir of the sequence to search. If multiple line possible, one can create multiple entry in the directory. 
#           For example, if two identical T1w are named either 't1 mprage' or 't1 mprage 3D', 2 lines need to be created with same bidsDir, bidsName but different line ID and datasetName
#   - bidsDir: name of the subdirectory containing the sequences (usually, anat, func or dwi)
#   - bidsName: new name for the sequence (eg: t1w to rename the T1w of subject 001 as sub-001_t1w.nii.gz)
dataOrganization = {1: {'datasetName': 'T1 MPRAGE 1mm isotropique', 'bidsDir': 'structural', 'bidsName': ''},
                    }

# Study name in Shanoir
studyIDToSearch = "LONGIDEP"
#studyIDToSearch = "MAPMS"

# SubjectID in Shanoir (put either the ID of the subject, multiple subjects ID separeted by a "OR" or a star (*) for all subjects)
subjectToSeach = "*"
#subjectToSeach = "*0110*"
#subjectToSeach = "(longidep*001*lm OR longidep*002*db OR longidep*003*sm)"

# ID of the line to process in dataOrganization dictionary                    
idSeq = [1]
#idSeq = range(1,3)

# Path of the output directory (where the BIDS-like directories should be created) (absolute or relative path (linked to where this Python file is located))
pathOutputDir = 'data/'

# Your ID on Shanoir
shanoirID = 'dsebastien'

# Type of data to download
fileType = 'dicom' #Alternative: 'dicom'
##############################################################################################
# / TO ADAPT
##############################################################################################


# Configure the parser and the configuration of the shanoir_downloader
parser = shanoir_downloader.create_arg_parser()
shanoir_downloader.add_arguments(parser)


# If a subjectID is given, first display all sequences available for this subject;
# this helps to check if there are new sequences in the protocol or if sequenceID is wrongly written
if subjectToSeach != "*":
    args = parser.parse_args(
        ['-u', shanoirID,
         '-d', 'shanoir.irisa.fr',
         '-of', pathOutputDir,
         '-em',
         '-st', 'studyName:' + studyIDToSearch +
         ' AND subjectName:' + subjectToSeach,
         '-s', '200',
         '-f', fileType,
         '-so', 'id,ASC'])

    config = shanoir_downloader.initialize(args)
    response = shanoir_downloader.solr_search(config, args)

    if response.status_code == 200:
        print('\n\nAvailable sequences for subject ' + subjectToSeach + ": ")
        
        for item in response.json()['content']:
            print('Subject ID: ' + item['subjectName'] + ' - Dataset Name:' + item["datasetName"])


# Loop on each sequences entered in idSeq
for idS in idSeq:
   
    # Arguments given by user at console or in the code
    if len(sys.argv) > 1:
        args = parser.parse_args()
    else:
        args = parser.parse_args(
            ['-u', shanoirID,
            '-d', 'shanoir.irisa.fr',
            '-of', pathOutputDir,
            '-em',
            '-st', 'studyName:' + studyIDToSearch + ' AND datasetName:\"' +
            dataOrganization[idS]['datasetName'] +
            '\" AND subjectName:' + subjectToSeach,
            '-s', '200',
            '-f', fileType,
            '-so', 'id,ASC'])

    config = shanoir_downloader.initialize(args)
    response = shanoir_downloader.solr_search(config, args)

    # From response, process the data
    # Print the number of items found and a list of these items
    if response.status_code == 200:
        print('\n SEQUENCE == ' + dataOrganization[idS]['datasetName'] + '\nnumber of items found: ' +
              str(len(response.json()['content'])))

        for item in response.json()['content']:
            print('Subject ID: ' + item['subjectName'] +
              ' - Dataset Name:' + item["datasetName"] + 
              ' - ID: ' + item['id'])

        # Download all data?
        input = 'y'  # input( 'Download everything? '  );

        if input in ['y', 'Y', 'yes', 'Yes', 'YES']:

            # Invoke shanoir_downloader to download all the data
            shanoir_downloader.download_search_results(config, args, response)


            # Organize in BIDS like specifications and rename files
            # Create subject directory
            for item in response.json()['content']:

                # ID of the subject (sub-*)
                subjID = item['subjectName'].replace(' ', '_').replace('LONGIDEP', 'lgp')
                print('Processing ' + subjID)

                subjDir = pathOutputDir + '/' + subjID 

                # Get the name of the downloaded archive
                dl_archive = glob.glob(
                    pathOutputDir + '/' + item['id'] + '*.zip')[0]

                # Create the directory of the subject
                Path(subjDir).mkdir(parents=True, exist_ok=True)
                # And create te subdirectories (ignore if exists)
                Path(subjDir + '/' +
                    dataOrganization[idS]['bidsDir']).mkdir(parents=True, exist_ok=True)
                

                # ***** Move Files*****
                # Check if the downloaded data has the good datasetName (should be always ok)
                if item['datasetName'].upper() == dataOrganization[idS]['datasetName'].upper():

                    # Check if images for this sequence already exist in the subdirectory of the subject
                    all_img = glob.glob(
                        subjDir + '/' + dataOrganization[idS]['bidsDir'] + '/' + subjID + '_' + dataOrganization[idS]['bidsName'] + '*.zip')

                    # If one image only exists, rename the previous one 'run-1' and the new one 'run-2'
                    if len(all_img) == 1:
                        os.rename(all_img[0], all_img[0].replace(
                            '.zip', '_run-1.zip'))
                        os.rename(glob.glob(pathOutputDir + '/*.zip')[0], subjDir + '/'+dataOrganization[idS]['bidsDir']+'/' + subjID +
                                '_' + dataOrganization[idS]['bidsName'] + '_run-2.zip')
                        
                    # Otherwise, if there is more than 2 images with 'run-*', rename the new one as a new run
                    # (eg, if run-1 and run-2 already exist, rename the new image as run-3)
                    elif len(all_img) > 1:
                        os.rename( dl_archive, subjDir + '/'+dataOrganization[idS]['bidsDir']+'/' + subjID +
                                '_' + dataOrganization[idS]['bidsName'] + '_run-' + str(len(all_img)+1) + '.zip')
                        
                    # Otherwise, if no image already available, rename the image without 'run-?'
                    else:
                        #print('subjID == ' + subjID)

                        os.rename( dl_archive, subjDir + '/'+dataOrganization[idS]['bidsDir']+'/' + subjID + '.zip')
                        

                else:
                    print('Nothing downloaded !')
    
    elif response.status_code == 204:
        
        print('\nNo file found!')
    else:
        print('\nError returned by the request: status of the response = ' + response.status_code)