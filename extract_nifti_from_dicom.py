import os
import sys
import zipfile
import subprocess

#
# Script to extract DICOM .zip files and convert them to NIFTI using dcm2niix. 
# Rename to appropriate file name.
# Then, move files to one directory before and delete all files that are not 
# .dcm in the DICOM folder.
#
# It takes bidsDir as an argument when launched, so you should precise whether
# you want to extract diffusion or structural folders.
#

dataFolder = 'data'

bidsDir = sys.argv[1]

for filename in os.listdir(dataFolder):
    pathToDicom = dataFolder + '/' + filename + '/' + bidsDir + '/' + 'dicom' # the last should be 'dicom'
    
    print(filename)
    with zipfile.ZipFile(dataFolder + '/' + filename + '/' + bidsDir + '/' + filename + '.zip', 'r') as zip_ref:
        zip_ref.extractall(path=pathToDicom)
        
    # conversion to NIFTI using dcm2niix
    subprocess.run(["~/Projects/softwares/dcm2niix/bin/bin/dcm2niix -m 1 -z 1 " + pathToDicom], 
                   shell=True)
    
    # rename .nii.gz and .bval files
    subprocess.run(["mv " '~/Projects/longidep/scripts/' + pathToDicom + '/*.bval ' + '~/Projects/longidep/scripts/' + pathToDicom + '/encoding_' + filename + '.bval'], 
                   shell=True)
    if bidsDir == 'diffusion':
        subprocess.run(["mv " '~/Projects/longidep/scripts/' + pathToDicom + '/*.nii.gz ' + '~/Projects/longidep/scripts/' + pathToDicom + '/dwi_' + filename + '.nii.gz'], 
                       shell=True)
    else:
        subprocess.run(["mv " '~/Projects/longidep/scripts/' + pathToDicom + '/*.nii.gz ' + '~/Projects/longidep/scripts/' + pathToDicom + '/T13D_' + filename + '.nii.gz'], 
                       shell=True)
    
    # move .nii.gz to one directory before
    subprocess.run(["mv " '~/Projects/longidep/scripts/' + pathToDicom + '/*.nii.gz ' + '~/Projects/longidep/scripts/' + dataFolder + '/' + filename + '/' + bidsDir + '/'], 
                   shell=True)
    
    if bidsDir == 'diffusion':
        # move .bval to one directory before
        subprocess.run(["mv " '~/Projects/longidep/scripts/' + pathToDicom + '/*.bval ' + '~/Projects/longidep/scripts/' + dataFolder + '/' + filename + '/' + bidsDir + '/'], 
                       shell=True)
    
    # delete files that are not .dcm in dicomFolder
    subprocess.run(["find " '~/Projects/longidep/scripts/' + pathToDicom + " -type f ! -name '*.dcm' -exec rm {} \;"], 
                   shell=True)
    
