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
dataOrganization = {1: {'datasetName': 'DIFF 30DIR b=1000s/mm2', 'bidsDir': 'diffusion', 'bidsName': ''}
                    }

# Study name in Shanoir
studyIDToSearch = "LONGIDEP"
#studyIDToSearch = "MAPMS"

# SubjectID in Shanoir (put either the ID of the subject, multiple subjects ID separeted by a "OR" or a star (*) for all subjects)
'''
subjectToSeach = ['longidep*001*lm',
'longidep*002*db',
'longidep*003*sm',
'longidep*004*di',
'longidep*005*pa',
'longidep*006*lc',
'longidep*007*tl',
'longidep*008*ag',
'longidep*009*it',
'longidep*010*fp',
'longidep*011*md',
'longidep*012*ck',
'longidep*013*rq',
'longidep*014*re',
'longidep*015*fs',
'longidep*016*lh',
'longidep*018*ah',
'longidep*020*gb',
'longidep*021*ms',
'longidep*022*de',
'longidep*023*pa',
'longidep*024*na',
'longidep*025*bj',
'longidep*026*le',
'longidep*027*ka',
'longidep*028*gy',
'longidep*029*va',
'longidep*031*em',
'longidep*032*do',
'longidep*033*hc',
'longidep*034*dc',
'longidep*035*db',
'longidep*036*qr',
'longidep*037*mp',
'longidep*037*mp',
'longidep*038*dv',
'longidep*039*bn',
'longidep*040*ss',
'longidep*041*ch',
'longidep*042*ab',
'longidep*043*ga',
'longidep*044*sd',
'longidep*045*ms',
'longidep*046*ar',
'longidep*047*cc',
'longidep*048*nd',
'longidep*049*cf',
'longidep*050*jb',
'longidep*051*mc',
'longidep*052*sl',
'longidep*053*mc',
'longidep*055*pmf',
'longidep*056*bd',
'longidep*057*dj',
'longidep*058*tp',
'longidep*059*le',
'longidep*060*dm',
'longidep*061*be',
'longidep*062*ps',
'longidep*063*cb',
'longidep*065*ls',
'longidep*066*hs',
'longidep*067*ls',
'longidep*068*mc',
'longidep*070*bo',
'longidep*071*la',
'longidep*073*df',
'longidep*073*rn',
'longidep*075*th',
'longidep*076*fo',
'longidep*077*bi',
'longidep*078*dm',
'longidep*079*lg',
'longidep*080*fd',
'longidep*081*ljp',
'longidep*082*mx',
'longidep*083*gc',
'longidep*084*lm',
'longidep*085*mr',
'longidep*086*ca',
'longidep*089*mc',
'longidep*090*vf',
'longidep*091*gm',
'longidep*092*rc',
'longidep*093*lj',
'longidep*095*ka',
'longidep*096*ms',
'longidep*097*jz',
'longidep*098*bn',
'longidep*099*fa',
'longidep*100*bv',
'longidep*101*mc',
'longidep*102*bn',
'longidep*103*do',
'longidep*104*ga',
'longidep*105*na',
'longidep*106*hh',
'longidep*107*be',
'longidep*108*mf',
'longidep*109*pa',
'longidep*110*lb',
'longidep*111*gl',
'longidep*113*ud',
'longidep*114*nm',
'longidep*115*lmr',
'longidep*116*lj',
'longidep*117*gp',
'longidep*118*tg',
'longidep*119*ln',
'longidep*120*ha',
'longidep*121*gs',
'longidep*122*lp',
'longidep*123*bs',
'longidep*124*jr',
'longidep*125*pg',
'longidep*126*lc',
'longidep*127*cc',
'longidep*128*cf',
'longidep*130*qc',
'longidep*131*mg',
'longidep*132*gs',
'longidep*134*he',
'longidep*135*cr',
'longidep*137*lm',
'longidep*138*pd',
'longidep*139*pmf',
'longidep*140*fm',
'longidep*141*rd',
'longidep*142*jo',
'longidep*143*ls',
'longidep*144*bc',
'longidep*145*ct',
'''
subjectToSeach = ['longidep*146*cv',
'longidep*147*mjc',
'longidep*148*lc',
'longidep*149*ch',
'longidep*150*hj',
'longidep*151*mm',
'longidep*152*bj',
'longidep*153*ml',
'longidep*154*lm',
'longidep*155*do.',
'longidep*156*gmt',
'longidep*157*cl',
'longidep*158*kh',
'longidep*159*ng',
'longidep*160*pr',
'longidep*161*md',
'longidep*162*cmc',
'longidep*163*bf',
'longidep*164*as',
'longidep*165*jj',
'longidep*166*re',
'longidep*168*ca',
'longidep*169*zc',
'longidep*169*zc',
'longidep*170*lm',
'longidep*171*ga',
'longidep*172*lc',
'longidep*173*gm',
'longidep*174*lp',
'longidep*175*pp',
'longidep*176*cj',
'longidep*177*dj',
'longidep*178*jb']

#subjectToSeach = "(longidep_001_lm OR longidep_002_db OR longidep_003_sm)"

# ID of the line to process in dataOrganization dictionary                    
idSeq = [1]
#idSeq = range(1,3)

# Path of the output directory (where the BIDS-like directories should be created) (absolute or relative path (linked to where this Python file is located))
pathOutputDir = 'data'

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
for subject in subjectToSeach:
    if subject != "*":
        args = parser.parse_args(
            ['-u', shanoirID,
             '-d', 'shanoir.irisa.fr',
             '-of', pathOutputDir,
             '-em',
             '-st', 'studyName:' + studyIDToSearch +
             ' AND subjectName:' + subject,
             '-s', '200',
             '-f', fileType,
             '-so', 'id,ASC'])

        config = shanoir_downloader.initialize(args)
        response = shanoir_downloader.solr_search(config, args)

        if response.status_code == 200:
            print('\n\nAvailable sequences for subject ' + subject + ": ")
            
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
                '\" AND subjectName:' + subject,
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
                    #dl_archive = glob.glob(
                    #    pathOutputDir + '/' + item['id'] + '*.zip')[0]
                    dl_archive = glob.glob(pathOutputDir + '/' + '*.zip')[0]

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
