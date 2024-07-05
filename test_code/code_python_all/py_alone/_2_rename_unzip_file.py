"""
================================================================================
File Name: _2_rename_unzip_file.py
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
Step 2: Rename the file
================================================================================

Function: rename_original_data

This function renames a file according to the date and time of data acquisition 
and the name of the person who collected the data.

Inside the folder, we can find the hierarchy of folders as follows:

    GeolocIMU_logger{year-month-day-hour-minute}
    
        -> {name of the person who collected the data}
    
            -> {day of the data collection}
            
                -> {hour of the data collection}
                
There are two types of dates: the date in the original name of the folder, which is when the data was sent to FileZilla,
and the date inside this folder, indicating when the data was precisely collected.

The root path of where to find the folder is ../data_treat/unzip

Input:
    fich (str): Name of the folder to be renamed.

Output:
    None
    
    
"""


def rename_original_data(fich):
    """
    @brief This function renames a file according to the date and time of data acquisition and the name of the person who collected the data.
    
    @param fich Name of the folder to be renamed.
    
    @return None
    """
   
    base1='../data_treat/unzip'  # Root path where to find the folder to be renamed
    
    personnes = os.listdir(f'{base1}/{fich}')  # Names of the people who collected the data
    for personne in personnes:
        days = os.listdir(f'{base1}/{fich}/{personne}')  # Days when the data was collected
        for day in days:
            hours = os.listdir(f'{base1}/{fich}/{personne}/{day}')  # Hours, minutes, and seconds when the data was collected
            for hour in hours:
                path_all = f'{base1}/{fich}/{personne}/{day}/{hour}'
    
                if personne == 'no name':  # If the person who collected the data is called 'no name', change it to 'none' to simplify the later treatment
                    per = 'none'
                else:
                    per = personne.lower() 
                
                name2 = f'{per}_{day.replace("-", "")}-{hour}'  # Final name of the folder
                
                # Create folder "rename" and the folder with the new name without the data in it if
                # not exist where to put the folder with the new name
                if not os.path.exists(f'../data_treat/rename/{name2}'): 
                    os.makedirs(f'../data_treat/rename/{name2}')
                
                if not os.path.exists(f'../data_original/data_before/{name2}'): 
                    os.makedirs(f'../data_original/data_before/{name2}')
                
                # Copy each file in the folder to the new folder with the new name
                for sensor in os.listdir(path_all):  
                    shutil.copy2(f'{path_all}/{sensor}', f'../data_original/data_before/{name2}')
                    shutil.copy2(f'{path_all}/{sensor}', f'../data_treat/rename/{name2}')
                    
    # Sometimes data was collected and renamed and there is no zip file so they were put into a folder 'data_before' 
    # and all the data in it are copied into the folder 'rename' to be treated as well as the data coming from the zip file
    for fich in os.listdir('../data_original/data_before'):
        if len(fich.split('_')) == 3:
            per = fich.split('_')[0]
            date = fich.split('_')[1]
            name_new = f'{per}_{date}'
            os.rename(f'../data_original/data_before/{fich}', f'../data_original/data_before/{name_new}')  
            fich = name_new
        if not os.path.exists(f'../data_treat/rename/{fich}'):
            shutil.copytree(f'../data_original/data_before/{fich}', f'../data_treat/rename/{fich}')
