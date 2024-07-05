"""
================================================================================
File Name: _1_unzip_file.py
Author: PARISOT Laura
Creation Date: 26/05/2024

================================================================================
"""



import zipfile  
import os  
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import shutil
import warnings 
warnings.filterwarnings('ignore')
warnings.filterwarnings("ignore", category=DeprecationWarning)


"""
================================================================================
Step 1: UNZIP the original file
================================================================================

Function: unzip_file

This function unzips a file given the name of the zip file. If needed, it creates 
a new folder called 'unzip' where it places the extracted files.
The path considered is ../data_original/zip

The zip data came from FileZilla when people send files via the GeolocIMUapp.

The zip file is named by the date of sending the data to FileZilla (year-month-day-hour-minute).

It also creates a folder 'root data_treat' if non-existent, where the data will be used later.
 It then copies the zip and unzipped files into their respective folders.

Input:
    name_file_zip (str): Name of the zip file (should end with .zip). Only the name, not the path.

Output:
    None
    
"""

def unzip_file(name_file_zip):
    """
     @brief This function unzips a file given the name of the zip file.
     
     @param name_file_zip Name of the zip file (should end with .zip).
     
     @return None
     """
     
    fich=name_file_zip
    path_original_zip='../data_original/zip'      #Path where to find the zip file
    path_original_unzip='../data_original/unzip'  #Path where to send the unzip file product
    
    if os.path.exists(f'{path_original_unzip}/{fich}'):        #Create a folder unzip if not exist yet
        os.makedirs(f'{path_original_unzip}/{fich[0:-4]}')
    
    #Unzip the original zip file and send it to the unzip folder
    with zipfile.ZipFile(f'{path_original_zip}/{fich}', 'r') as zip_ref:  
        zip_ref.extractall(f'{path_original_unzip}/{fich[0:-4]}')
    
    
    if not os.path.exists(f'../data_treat/unzip'):  #Create a folder into the folder data treat for unzip file
        os.makedirs(f'../data_treat/unzip')
        
    if not os.path.exists(f'../data_treat/unzip/{fich[0:-4]}'):  #Copy the unzip file to the root folder data_treat
        shutil.copytree(f'../data_original/unzip/{fich[0:-4]}', f'../data_treat/unzip/{fich[0:-4]}')
        
    if not os.path.exists(f'../data_treat/zip'):  #Create a folder into the folder data treat for zip file
        os.makedirs(f'../data_treat/zip')
        
    if not os.path.exists(f'../data_treat/zip/{fich}'):  #Copy the zip file to the root folder data_treat
        shutil.copy2(f'../data_original/zip/{fich}', f'../data_treat/zip/{fich}')