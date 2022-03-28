# dicom_to_nifti
Process to convert DICOM to NIFTI with correction on bvecs via Anima.

# Files 

* download_data_on_Shanoir_and_BIDS_reorganisation.py : Script to download and BIDS-like organize data on Shanoir using ”shanoir downloader.py” developed by Arthur Masson. Codes provided by Malo Gaubert. Downloads archive with DICOM files as zip files in the folder `dicom` ;

* download_data_on_Shanoir_and_BIDS_reorganisation_diffusion.py : Script adapted from the previous one to download diffusion data. This file is needed to cope with datasets whose name includes a `/`. Otherwise, as the script sequentially downloads files, each of them is named the same way and it would result in a single file downloaded at the end. As a result, all of the subjects were added in a list (copied pasted from an Excel file) as well as a `For` loop to rename .zip files ;

* shanoir downloader.py : Needed to download data from Shanoir, see [GitHub](https://github.com/Inria-Empenn/shanoir_downloader) ;

* extract_nifti_from_dicom.py : Script to extract DICOM .zip files and convert them to NIFTI using dcm2niix. The important files are the ones with the extensions .dcm, .bval, .nii.gz ;

* modifiedAnimaDiffusionPreprocessing_Sebastien_flip.py (to rename later) : Script adapted from [animaDiffusionImagePreprocessing.py](https://github.com/Inria-Empenn/Anima-Scripts-Public/blob/master/diffusion/animaDiffusionImagePreprocessing.py) from Anima-Scripts. The changes added consist in taking the 31 first rows of bvecs corrected and change some extensions from .nii.gz format to .nrrd.

# Process 

1. Download DICOM files on Shanoir :
python ./download_data_on_Shanoir_and_BIDS_reorganisation.py and type the password
2. (optional) If diffusion DICOM files are downloaded :
python ./download_data_on_Shanoir_and_BIDS_reorganisation_diffusion.py and type your password
3. Run python ./extract_nifti_from_dicom.py diffusion (may need to replace diffusion with another name of the subdirectory containing the sequences)
4. Upload these files on Igrida : `scp -r path to dicom folder user @igrida-frontend:some_path`
