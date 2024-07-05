"""
================================================================================
File Name: __main.py
Author: PARISOT Laura
Creation Date: 26/05/2024
Description: 
    This file serves as the main entry point of our project.
    It includes all the necessary functions to process data related to the problem 
    of floor-changing activity. It launches functions, creates folders, and manages/treats 
    the data to ultimately obtain the best classification model between five classes: 
    walk, still, elevator, escalator, and stair, using data obtained from the GeolocIMU app.
    
    The main responsibilities of this file include:
    1. Processing the original data to create an input for feature extraction.
    2. Launching the feature extraction and feature selection stages.
    3. Training multiple machine learning models to obtain the best possible model.

Usage:
    To run this file, use the following command:
    $ python __main.py

Modification History:
    //

================================================================================
"""


"""
================================================================================
Importing Libraries
================================================================================
"""
import onnxruntime
import os
import zipfile
import shutil
import subprocess
import warnings
warnings.filterwarnings('ignore')
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Data handling
import pandas as pd
import numpy as np
import random
from inputimeout import inputimeout, TimeoutOccurred
# Visualization
import matplotlib.pyplot as plt
import seaborn as sns

# Timing
import time

# Scikit-learn for machine learning
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.feature_selection import mutual_info_classif
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix

# Model export and conversion
from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import FloatTensorType
import onnx
import onnxmltools
from onnxmltools.convert.common.data_types import FloatTensorType
import tf2onnx
import def_test
# XGBoost for gradient boosting
from xgboost import XGBClassifier

# TensorFlow and Keras for deep learning
import tensorflow as tf
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)
from tensorflow.keras.layers import (Input, Conv1D, MaxPooling1D, GlobalAveragePooling1D, Dense,
                                     Dropout, BatchNormalization, Flatten, GlobalMaxPooling1D)
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.models import Model
from keras.models import load_model
from tensorflow.keras.optimizers import Adam, SGD
from tensorflow.keras.callbacks import ReduceLROnPlateau
import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.optimizers import Adam
from sklearn.svm import SVC
from sklearn.metrics import classification_report, accuracy_score
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

        
        
"""
================================================================================
Step 3: Interpolate the file
================================================================================

Function: interpolation_of_data_rename

This function takes the renamed data and interpolates the sensor data to the same time 
acquisition, specifically the accelerometer time acquisition, and saves the processed data 
in a different folder.

Input: 
    folder (str): Name of the folder containing the data to be interpolated according 
                  to the accelerometer time.

Output:
    None
    
"""

def interpolation_of_data_rename(folder):
    
    path=rf"../data_treat/rename/{folder}"  #Root path where to find folder where whithin there is the data collect for each sensor considered
    
    #Data for the accelrometer
    data_acc=pd.read_csv(f"{path}/ACC.txt", delimiter=',', header=None, index_col=None,skiprows=1)
    
    #Time of the accelerometerer that will be used to interpolate the data of the other sensor
    t_acc=data_acc.iloc[:,1]
    
    #List of the activity link to each time of acquisition of the accelerometer data
    modie=np.array(data_acc.iloc[:, 0])
    
    #If the list of activity is all nan, dont contune the code
    if all(isinstance(element, float) for element in modie):
        return 0
    
    #Change the name if the activity is nan and change the activity lift to elevator
    for i, m in enumerate(modie):
        if isinstance(m, float) and pd.isna(m):
            modie[i] = 'unknown'
        elif isinstance(m, str):
            if m == 'lift':
                modie[i] = 'elevator'
            elif m == 'nan':
                modie[i] = 'unknown'
                
    
    #Now considered the list of activity as an dataframe
    modie=pd.DataFrame(modie)
    
    #List of the step done at the time of each acquisition as a Dataframe
    pas=data_acc.iloc[:,8]
    
    #Data for the other sensor gyroscope , magnetometer et barometer
    data_gyr = pd.read_csv(rf'{path}\GYR.txt', delimiter=',', header=None, index_col=None,skiprows=1)
    data_mag = pd.read_csv(rf'{path}\MAG.txt', delimiter=',', header=None, index_col=None,skiprows=1)
    data_baro=pd.read_csv(rf'{path}\BARO.txt', delimiter=',', header=None, index_col=None,skiprows=1)
    
    #Take the time acquition for each sensor
    t_acc = data_acc.iloc[:, 1].astype(float)
    t_mag = data_mag.iloc[:, 1].astype(float)
    t_gyr = data_gyr.iloc[:, 1].astype(float)
    t_baro = data_baro.iloc[:, 1].astype(float)
    
    #Interpolate the data accoridng to the time of acquisiton of the accelrometer data
    data_mag_inter = np.column_stack([
        np.interp(t_acc, t_mag, data_mag.iloc[:, i].astype(float)) for i in range(2, 5)
    ])
    data_mag_inter = np.column_stack((modie,t_acc,data_mag_inter,pas))
    
    data_gyr_inter = np.column_stack([
        np.interp(t_acc, t_gyr, data_gyr.iloc[:, i].astype(float)) for i in range(2, 5)
    ])
    data_gyr_inter = np.column_stack((modie,t_acc,data_gyr_inter,pas))
    
    data_baro_inter = np.column_stack([
        np.interp(t_acc, t_baro, data_baro.iloc[:, 2].astype(float))
    ])
    data_baro_inter = np.column_stack((modie,t_acc,data_baro_inter,pas))
    
    data_acc_inter=np.column_stack((modie,t_acc,data_acc.iloc[:, 3:6],pas))


    data_acc,data_gyr,data_mag,data_baro=data_acc_inter,data_gyr_inter,data_mag_inter,data_baro_inter

    #Create the data frame organised the same way for each sensor on the same basis of time
    data_acc=pd.DataFrame(data_acc,columns=['mode','time','acc_x','acc_y','acc_z','nb_step'])
    data_gyr=pd.DataFrame(data_gyr,columns=['mode','time','gyr_x','gyr_y','gyr_z','nb_step'])
    data_mag=pd.DataFrame(data_mag,columns=['mode','time','mag_x','mag_y','mag_z','nb_step'])
    data_baro=pd.DataFrame(data_baro,columns=['mode','time','pressure','nb_step'])
    
    
    #reindexing on the same base the dataframe for each sensor
    data_acc.reset_index(drop=True, inplace=True)
    data_mag.reset_index(drop=True, inplace=True)
    data_baro.reset_index(drop=True, inplace=True)
    data_gyr.reset_index(drop=True, inplace=True)
    
    #Re-extract the activity considered fo each time of acquisition
    mode=np.array(data_acc.iloc[:,0])
    
    #Search the index where the activity change considered the previous activity
    indices_changement_valeurs = indices_changement(mode)
    # for i in range(1, len(mode)):
    #     if mode[i] != mode[i-1]:
    #         indices_changement_valeurs.append(i)
   

    
    #If for all the acquition there is only one activty considered save the data directly
    if len(indices_changement_valeurs)==0:
        mode=data_acc.iloc[0,0]
        if mode!='unknown':
            if not os.path.exists(f'../data_treat/data_interpolate_base/{folder}_{mode}_0'):
                os.makedirs(f'../data_treat/data_interpolate_base/{folder}_{mode}_0') 
            
            data_acc.to_csv(f'../data_treat/data_interpolate_base/{folder}_{mode}_0/ACC.txt',header=True,index=False)
            data_gyr.to_csv(f'../data_treat/data_interpolate_base/{folder}_{mode}_0/GYR.txt',header=True,index=False)
            data_mag.to_csv(f'../data_treat/data_interpolate_base/{folder}_{mode}_0/MAG.txt',header=True,index=False)
            data_baro.to_csv(f'../data_treat/data_interpolate_base/{folder}_{mode}_0/BARO.txt',header=True,index=False)
                 
            df=pd.concat([data_acc,data_gyr,data_mag,data_baro],axis=1)  
            df = df.loc[:, ~df.columns.duplicated()]
            
            new_order = ['mode','acc_x','acc_y','acc_z','gyr_x','gyr_y','gyr_z','mag_x','mag_y','mag_z','pressure','time','nb_step']
            df=df[new_order]
            if not os.path.exists(f'../data_treat/data_interpolate'):
                os.makedirs(f'../data_treat/data_interpolate') 
            df.to_csv(f'../data_treat/data_interpolate/{folder}_{mode}_0.txt',header=True,index=False)        
                    
    #If there is mutiple activyt collect durin the acquisition extract the data for each activity and
    #save the data extraction
    else:
        indices_changement_valeurs.insert(0,0)
        for i in range(len(indices_changement_valeurs)):
            
            if i!=len(indices_changement_valeurs)-1:
                i_0=indices_changement_valeurs[i]
                i_1=indices_changement_valeurs[i+1]
                
                
                data_acc_inter=data_acc.iloc[i_0:i_1,:]
                data_gyr_inter=data_gyr.iloc[i_0:i_1,:]
                data_mag_inter=data_mag.iloc[i_0:i_1,:]
                data_baro_inter=data_baro.iloc[i_0:i_1,:]
                
            else:
                i_0=indices_changement_valeurs[i]
            
                data_acc_inter=data_acc.iloc[i_0:,:]
                data_gyr_inter=data_gyr.iloc[i_0:,:]
                data_mag_inter=data_mag.iloc[i_0:,:]
                data_baro_inter=data_baro.iloc[i_0:,:]
            
            
            mode=data_acc_inter.iloc[0,0]
            if mode!='unknown':
                if not os.path.exists(f'../data_treat/data_interpolate_base/{folder}_{mode}_{i}'):
                    os.makedirs(f'../data_treat/data_interpolate_base/{folder}_{mode}_{i}')     
                    
                    
                data_acc_inter.to_csv(f'../data_treat/data_interpolate_base/{folder}_{mode}_{i}/ACC.txt',header=True,index=False)
                data_gyr_inter.to_csv(f'../data_treat/data_interpolate_base/{folder}_{mode}_{i}/GYR.txt',header=True,index=False)
                data_mag_inter.to_csv(f'../data_treat/data_interpolate_base/{folder}_{mode}_{i}/MAG.txt',header=True,index=False)
                data_baro_inter.to_csv(f'../data_treat/data_interpolate_base/{folder}_{mode}_{i}/BARO.txt',header=True,index=False)
                     
                df=pd.concat([data_acc_inter,data_gyr_inter,data_mag_inter,data_baro_inter],axis=1)  
                df = df.loc[:, ~df.columns.duplicated()]
                
                new_order = ['mode','acc_x','acc_y','acc_z','gyr_x','gyr_y','gyr_z','mag_x','mag_y','mag_z','pressure','time','nb_step']
                df=df[new_order]
                if not os.path.exists(f'../data_treat/data_interpolate'):
                    os.makedirs(f'../data_treat/data_interpolate') 
                df.to_csv(f'../data_treat/data_interpolate/{folder}_{mode}_{i}.txt',header=True,index=False)   
                
                
            

       

                 
"""
================================================================================
Step BIS: Visualize Original Data
================================================================================

Function: visu_data

This function visualizes the collected data. The data should be interpolated to 
the same timeline. It saves the graphics in a specific folder according to the 
activity practiced.

Input:
    
    chemin (str): Name of the folder containing the data.
    file (str) : ..

Output:
    None
"""

def visu_data(chemin,file):
    """
   @brief This function visualizes the collected data.
   
   @param dataframe DataFrame containing the sensor data to be visualized.
   @param chemin Name of the folder containing the data.
   
   @return None
   """
    #Getting the data for each sensor
    data_acc=pd.read_csv(f'{chemin}/ACC.txt',header=0)
    data_gyr=pd.read_csv(f'{chemin}/GYR.txt',header=0)
    data_mag=pd.read_csv(f'{chemin}/MAG.txt',header=0)
    data_baro=pd.read_csv(f'{chemin}/BARO.txt',header=0)
    
    #Getting the maximum and minimum for each sensor to equalize te visualization of the plot on the same basis of axis
    
    max_acc_x = data_acc.iloc[:, 2].max()+1
    max_acc_y = data_acc.iloc[:, 3].max()+1
    max_acc_z = data_acc.iloc[:, 4].max()+1
    
    max_gyr_x = data_gyr.iloc[:, 2].max()+1
    max_gyr_y = data_gyr.iloc[:, 3].max()+1
    max_gyr_z = data_gyr.iloc[:, 4].max()+1
    
    max_mag_x = data_mag.iloc[:, 2].max()+1
    max_mag_y = data_mag.iloc[:, 3].max()+1
    max_mag_z = data_mag.iloc[:, 4].max()+1
    
    min_acc_x = data_acc.iloc[:, 2].min()-1
    min_acc_y = data_acc.iloc[:, 3].min()-1
    min_acc_z = data_acc.iloc[:, 4].min()-1
    
    min_gyr_x = data_gyr.iloc[:, 2].min()-1
    min_gyr_y = data_gyr.iloc[:, 3].min()-1
    min_gyr_z = data_gyr.iloc[:, 4].min()-1
    
    min_mag_x = data_mag.iloc[:, 2].min()-1
    min_mag_y = data_mag.iloc[:, 3].min()-1
    min_mag_z = data_mag.iloc[:, 4].min()-1
    
    
    nom_dossier = os.path.basename(chemin)
    
    #Getting the name , mode and people of the data to make the name and title of the plot
    parties = nom_dossier.split('_')
    if parties[0]=='no':
        parties=['no_name',parties[2],parties[3]]
    personne = parties[0]
    date = parties[1]
    type_activite =parties[2] 
    print("Chemin:", chemin)
    print("Personne:", personne)
    print("Date:", date)
    print("Type d'activité:", type_activite)
    print()
    
    #Title of the plot
    titre=fr"{type_activite.upper()} Date : {date}  Personne : {personne}"
    
    #Making the plots considering the position and data to vizualisation
    fig, axs = plt.subplots(4, 4, figsize=(14, 10))
    axs[1, 3].plot(data_baro.iloc[:,1], data_baro.iloc[:,2], label='Pressure [hPa]', color='violet')
    axs[1, 3].legend()
    axs[1, 3].set_xlabel('Temps [s]')
    axs[1, 3].set_title('Baro data')
    
    axs[0, 3].plot(data_acc.iloc[:,1], data_acc.iloc[:,5], label='Number of Step', color='violet')
    axs[0, 3].legend()
    axs[0, 3].set_xlabel('Temps [s]')
    axs[0, 3].set_title('Step data')
    
    
    fig.delaxes(axs[2, 3])
    fig.delaxes(axs[3, 3])
    
    
    

    axs[0,0].plot(data_acc.iloc[:,1], data_acc.iloc[:,2], label='Accx [m/s2]',color='g')
    axs[0,0].set_title('ACC Data')
    axs[0, 0].set_xlabel('Temps [s]')
    axs[0,0].set_ylim(min_acc_x,max_acc_x)
    axs[0,0].legend()
    
    axs[1,0].plot(data_acc.iloc[:,1], data_acc.iloc[:,3], label='Accy [m/s2]',color='r')
    axs[1,0].set_ylim(min_acc_y,max_acc_y)
    axs[1,0].set_xlabel('Temps [s]')
    axs[1,0].legend()
    
    
    axs[2,0].plot(data_acc.iloc[:,1], data_acc.iloc[:,4], label='Accz [m/s2]',color='b')
    axs[2,0].set_ylim(min_acc_z,max_acc_z)
    axs[2,0].set_xlabel('Temps [s]')
    axs[2,0].legend()
    
    axs[3,0].plot(data_acc.iloc[:,1], np.sqrt(data_acc.iloc[:,4]**2+data_acc.iloc[:,3]**2+data_acc.iloc[:,2]**2), label='Norme Acc [m/s2]',color='c')
    axs[3,0].set_xlabel('Temps [s]')
    axs[3,0].legend()
    
    
    
    axs[0,1].plot(data_gyr.iloc[:,1], data_gyr.iloc[:,2], label='Gyrx [rad/s]',color='g')
    axs[0,1].set_title('GYR Data')
    axs[0,1].set_ylim(min_gyr_x,max_gyr_x)
    axs[0,1].set_xlabel('Temps [s]')
    axs[0,1].legend()
    
    axs[1,1].plot(data_gyr.iloc[:,1], data_gyr.iloc[:,3], label='Gyrcy [rad/s]',color='r')
    axs[1,1].set_ylim(min_gyr_y,max_gyr_y)
    axs[1,1].set_xlabel('Temps [s]')
    axs[1,1].legend()
    
    axs[2,1].plot(data_gyr.iloc[:,1], data_gyr.iloc[:,4], label='Gyrz [rad/s]',color='b')
    axs[2,1].set_ylim(min_gyr_z,max_gyr_z)
    axs[2,1].set_xlabel('Temps [s]')
    axs[2,1].legend()
    
    axs[3,1].plot(data_gyr.iloc[:,1], np.sqrt(data_gyr.iloc[:,4]**2+data_gyr.iloc[:,3]**2+data_gyr.iloc[:,2]**2), label='Norme Gyr [rad/s]',color='c')
    axs[3,1].set_xlabel('Temps [s]')
    axs[3,1].legend()
    
    
    
    
    
    axs[0,2].plot(data_mag.iloc[:,1], data_mag.iloc[:,2], label='Magx [μT]',color='g')
    axs[0,2].set_title('Mag Data')
    axs[0,2].set_ylim(min_mag_x,max_mag_x)
    axs[0,2].set_xlabel('Temps [s]')
    axs[0,2].legend()
    
    axs[1,2].plot(data_mag.iloc[:,1], data_mag.iloc[:,3], label='Magcy [μT]',color='r')
    axs[1,2].set_ylim(min_mag_y,max_mag_y)
    axs[1,2].set_xlabel('Temps [s]')
    axs[1,2].legend()
    
    axs[2,2].plot(data_mag.iloc[:,1], data_mag.iloc[:,4], label='Magz [μT]',color='b')
    axs[2,2].set_ylim(min_mag_z,max_mag_z)
    axs[2,2].set_xlabel('Temps [s]')
    axs[2,2].legend()
    
    axs[3,2].plot(data_mag.iloc[:,1], np.sqrt(data_mag.iloc[:,4]**2+data_mag.iloc[:,3]**2+data_mag.iloc[:,2]**2), label='Norme Mag [μT]',color='c')
    axs[3,2].set_xlabel('Temps [s]')
    axs[3,2].legend()
    
    plt.suptitle(titre)
    plt.tight_layout()
    
    #Saving the pot on a specifics folder
    
    if not os.path.exists(f'../data_treat/graphics/{str(type_activite)}/'):
            os.makedirs(f'../data_treat/graphics/{str(type_activite)}/')
    
    file2=file.replace('-',"_")
    plt.savefig(f'../data_treat/graphics/{str(type_activite)}/{file2}.png')
    plt.show()
    




"""
================================================================================
Step 4: Sort Data According to Step Count
================================================================================

Function: sort_data_by_step

This function sorts the data to identify and exclude errors during data collection. 
It is based on the number of steps taken during the activity.

For activities like 'escalator', 'elevator', or 'still', a low number of steps 
should be recorded during the acquisition. If there are more than 3 steps recorded, 
the acquisition line with step count exceeding 3 is deleted.

Conversely, for activities like 'stair' or 'walk', a considerable number of steps 
should be recorded. If there are 0 or 1 steps recorded during the entire acquisition 
time, the file is not considered.

This function creates a specific folder containing all the files with the sorted data.

Input:
    None

Output:
    None
"""




def indices_changement(liste):
    """
    @brief This fonction bis is used to get the index where there is a change in a list data.
    @return None
    """
    indices = [] #Initiaization of the index list 
    #If the element at i position is differnet to the element at i-1 psotion , we add the index i to the list
    for i in range(1, len(liste)): #Browse the liste by index represented by i
        if liste[i] != liste[i-1]: 
            indices.append(i)
    return indices


                
#Sorting the data according to the number of step and mode that they represent

def sort_data_by_step():
    """
    @brief This function sorts the data to identify and exclude errors during data collection based on the number of steps taken during the activity.
   
    @return None
    """
    print('Begin of the sorting by step')
    
    # Initialize the boolean to not save the data if no condition is fulfilled
    save = False
    length=len(os.listdir('../data_treat/data_interpolate'))
    
    list_baro_change=[]
    # Browse through all the data 
    for enu,fich in enumerate(os.listdir('../data_treat/data_interpolate')):
        save=False
        # Get the data in a dataframe to help with the process
        data = pd.read_csv(f'../data_treat/data_interpolate/{fich}')
        
        # Automatically remove the first and last 20% of the data
        
        data.reset_index(drop=True, inplace=True)
        
        data['time'] = data['time'] - data['time'][0]
        data['nb_step'] = data['nb_step'] - data['nb_step'][0]
        
        # Get the label of the data
        mode = str(data['mode'][0])
        
        step=data['nb_step'].values
        u,c=np.unique(step,return_counts=True)
        
        time=data['time'].values
        
        baro=data['pressure'].values
        
        data_list=[]
        
        
        if mode=='escalator' or mode=='elevator' or mode=="still":
            
            if len(c)==1:
                if time[-1]>3:
                    data_list.append(data)
                    save=True
                    
            else:
                where2=np.where(c>500)[0]
                for where in where2:
                    step_where=np.where(step==u[where])[0]
                    data_bis=data.iloc[step_where,:]
                    data_bis.reset_index(drop=True, inplace=True)
                    data_bis['time'] = data_bis['time'] - data_bis['time'][0]
                    data_bis['nb_step'] = data_bis['nb_step'] - data_bis['nb_step'][0]
                    
                    if time[-1]>3:
                        data_list.append(data_bis)
                        save=True
                        
        if mode=='stair' or mode=='walk':
            
            where2=np.where((c > 150) | (c < 10))[0]
            list_step_non=[]
            if len(where2)>0:
                for where in where2:
                    step_non=np.where(step==u[where])[0]
                    list_step_non.append(list(step_non))
            
            if list_step_non==[]:
                data_list.append(data)
                save=True
                
            else:
                
                indice_debut=[]
                indice_fin=[]
                
                for l in list_step_non:
                    indice_debut.append(l[0])
                    indice_fin.append(l[len(l)-1])

                for i in range(0,len(indice_debut)-1):
                    
                    data_bis=data.iloc[indice_fin[i]+1:indice_debut[i+1]-1,:]
                    
                    if len(data_bis)>0:
                            
                        data_bis.reset_index(drop=True, inplace=True)
                        data_bis['time'] = data_bis['time'] - data_bis['time'][0]
                        data_bis['nb_step'] = data_bis['nb_step'] - data_bis['nb_step'][0]
                        
                        step2=data_bis['nb_step'].values
                        u2,c2=np.unique(step2,return_counts=True)
                        if len(c2)>3:
                            data_list.append(data_bis)
                            save=True
        
   
        
        if save:
        
            if not os.path.exists(f'../data_treat/data_interpolate_sorted'):
                os.makedirs(f'../data_treat/data_interpolate_sorted')
                
            for ii,data_app in enumerate(data_list):
                
                data_app.to_csv(f'../data_treat/data_interpolate_sorted/{fich.split(".")[0]}_sort{ii}.txt', header=False, index=False)

            
"""
================================================================================
Step BIS: Visualize Sorted Data
================================================================================

Function: visu_data_sorted

This function visualizes the data collected after sorting. The data should be 
interpolated to the same timeline. It saves the graphics in a specific folder 
according to the activity practiced.

Input:
    chemin (str): Name of the folder containing the data.
    file (str): Name of the file for saving the graphics made.

Output:
    None
"""

def visu_data_sorted(chemin, file):
    """
    @brief The function permits to visualize the data after being sorted according to step count and the mode
    
    @param chemin: path to find the data
    @param file: Name of the PNG file that will be saved
    @return None
    """
    data = pd.read_csv(chemin)
    data.columns=new_order = ['mode','acc_x','acc_y','acc_z','gyr_x','gyr_y','gyr_z','mag_x','mag_y','mag_z','pressure','time','nb_step']
    
    
    # Separate the data into different dataframes based on the type of measurement
    data_acc = data[['mode', 'time', 'acc_x', 'acc_y', 'acc_z', 'nb_step']]
    data_gyr = data[['mode', 'time', 'gyr_x', 'gyr_y', 'gyr_z', 'nb_step']]
    data_mag = data[['mode', 'time', 'mag_x', 'mag_y', 'mag_z', 'nb_step']]
    data_baro = data[['mode', 'time', 'pressure', 'nb_step']]

    # Calculate max and min values for setting plot limits
    max_acc_x = data_acc.iloc[:, 2].max() + 1
    max_acc_y = data_acc.iloc[:, 3].max() + 1
    max_acc_z = data_acc.iloc[:, 4].max() + 1
    
    max_gyr_x = data_gyr.iloc[:, 2].max() + 1
    max_gyr_y = data_gyr.iloc[:, 3].max() + 1
    max_gyr_z = data_gyr.iloc[:, 4].max() + 1
    
    max_mag_x = data_mag.iloc[:, 2].max() + 1
    max_mag_y = data_mag.iloc[:, 3].max() + 1
    max_mag_z = data_mag.iloc[:, 4].max() + 1
    
    min_acc_x = data_acc.iloc[:, 2].min() - 1
    min_acc_y = data_acc.iloc[:, 3].min() - 1
    min_acc_z = data_acc.iloc[:, 4].min() - 1
    
    min_gyr_x = data_gyr.iloc[:, 2].min() - 1
    min_gyr_y = data_gyr.iloc[:, 3].min() - 1
    min_gyr_z = data_gyr.iloc[:, 4].min() - 1
    
    min_mag_x = data_mag.iloc[:, 2].min() - 1
    min_mag_y = data_mag.iloc[:, 3].min() - 1
    min_mag_z = data_mag.iloc[:, 4].min() - 1
    
    # Extract the folder name from the path
    nom_dossier = os.path.basename(chemin)
    
    # Split the folder name to get details about the data
    parties = nom_dossier.split('_')
    if parties[0] == 'no':
        parties = ['no_name', parties[2], parties[3]]
    personne = parties[0]
    date = parties[1]
    type_activite = parties[2].split(".")[0]
    print("Chemin:", chemin)
    print("Personne:", personne)
    print("Date:", date)
    print("Type d'activité:", type_activite.split(".")[0])
    print()
    
    # Title for the plots
    titre = fr"{type_activite.upper()} Date : {date}  Personne : {personne}"
    
    # Create subplots for visualization
    fig, axs = plt.subplots(4, 4, figsize=(14, 10))
    
    # Plot barometer data
    axs[1, 3].plot(data_baro.iloc[:, 1], data_baro.iloc[:, 2], label='Pressure [hPa]', color='violet')
    axs[1, 3].legend()
    axs[1, 3].set_xlabel('Time [s]')
    axs[1, 3].set_title('Barometer Data')
    
    # Plot step data
    axs[0, 3].plot(data_acc.iloc[:, 1], data_acc.iloc[:, 5], label='Number of Steps', color='violet')
    axs[0, 3].legend()
    axs[0, 3].set_xlabel('Time [s]')
    axs[0, 3].set_title('Step Data')
    
    # Remove unused subplots
    fig.delaxes(axs[2, 3])
    fig.delaxes(axs[3, 3])
    
    # Plot accelerometer data
    axs[0, 0].plot(data_acc.iloc[:, 1], data_acc.iloc[:, 2], label='Accx [m/s²]', color='g')
    axs[0, 0].set_title('Accelerometer Data')
    axs[0, 0].set_xlabel('Time [s]')
    axs[0, 0].set_ylim(min_acc_x, max_acc_x)
    axs[0, 0].legend()
    
    axs[1, 0].plot(data_acc.iloc[:, 1], data_acc.iloc[:, 3], label='Accy [m/s²]', color='r')
    axs[1, 0].set_ylim(min_acc_y, max_acc_y)
    axs[1, 0].set_xlabel('Time [s]')
    axs[1, 0].legend()
    
    axs[2, 0].plot(data_acc.iloc[:, 1], data_acc.iloc[:, 4], label='Accz [m/s²]', color='b')
    axs[2, 0].set_ylim(min_acc_z, max_acc_z)
    axs[2, 0].set_xlabel('Time [s]')
    axs[2, 0].legend()
    
    axs[3, 0].plot(data_acc.iloc[:, 1], np.sqrt(data_acc.iloc[:, 4]**2 + data_acc.iloc[:, 3]**2 + data_acc.iloc[:, 2]**2), label='Acc Norm [m/s²]', color='c')
    axs[3, 0].set_xlabel('Time [s]')
    axs[3, 0].legend()
    
    # Plot gyroscope data
    axs[0, 1].plot(data_gyr.iloc[:, 1], data_gyr.iloc[:, 2], label='Gyrx [rad/s]', color='g')
    axs[0, 1].set_title('Gyroscope Data')
    axs[0, 1].set_ylim(min_gyr_x, max_gyr_x)
    axs[0, 1].set_xlabel('Time [s]')
    axs[0, 1].legend()
    
    axs[1, 1].plot(data_gyr.iloc[:, 1], data_gyr.iloc[:, 3], label='Gyry [rad/s]', color='r')
    axs[1, 1].set_ylim(min_gyr_y, max_gyr_y)
    axs[1, 1].set_xlabel('Time [s]')
    axs[1, 1].legend()
    
    axs[2, 1].plot(data_gyr.iloc[:, 1], data_gyr.iloc[:, 4], label='Gyrz [rad/s]', color='b')
    axs[2, 1].set_ylim(min_gyr_z, max_gyr_z)
    axs[2, 1].set_xlabel('Time [s]')
    axs[2, 1].legend()
    
    axs[3, 1].plot(data_gyr.iloc[:, 1], np.sqrt(data_gyr.iloc[:, 4]**2 + data_gyr.iloc[:, 3]**2 + data_gyr.iloc[:, 2]**2), label='Gyr Norm [rad/s]', color='c')
    axs[3, 1].set_xlabel('Time [s]')
    axs[3, 1].legend()
    
    # Plot magnetometer data
    axs[0, 2].plot(data_mag.iloc[:, 1], data_mag.iloc[:, 2], label='Magx [μT]', color='g')
    axs[0, 2].set_title('Magnetometer Data')
    axs[0, 2].set_ylim(min_mag_x, max_mag_x)
    axs[0, 2].set_xlabel('Time [s]')
    axs[0, 2].legend()
    
    axs[1, 2].plot(data_mag.iloc[:, 1], data_mag.iloc[:, 3], label='Magy [μT]', color='r')
    axs[1, 2].set_ylim(min_mag_y, max_mag_y)
    axs[1, 2].set_xlabel('Time [s]')
    axs[1, 2].legend()
    
    axs[2, 2].plot(data_mag.iloc[:, 1], data_mag.iloc[:, 4], label='Magz [μT]', color='b')
    axs[2, 2].set_ylim(min_mag_z, max_mag_z)
    axs[2, 2].set_xlabel('Time [s]')
    axs[2, 2].legend()
    
    axs[3, 2].plot(data_mag.iloc[:, 1], np.sqrt(data_mag.iloc[:, 4]**2 + data_mag.iloc[:, 3]**2 + data_mag.iloc[:, 2]**2), label='Mag Norm [μT]', color='c')
    axs[3, 2].set_xlabel('Time [s]')
    axs[3, 2].legend()
    
    # Set the main title for the plots
    plt.suptitle(titre)
    plt.tight_layout()
    
    # Create directory if it does not exist
    if not os.path.exists(f'../data_treat/graphics_sorted/{str(type_activite).split(".")[0]}'):
        os.makedirs(f'../data_treat/graphics_sorted/{str(type_activite).split(".")[0]}')
    
    # Save the figure
    plt.savefig(f'../data_treat/graphics_sorted/{str(type_activite).split(".")[0]}/{file.split(".")[0]}.png')
    plt.show()
    
"""
================================================================================
# Step 5: Separate Data by Step or Second
================================================================================

# Function: separate_data_by_step_or_second

# This function splits the input data for the feature extractor stage. It proceeds 
# by considering two approaches: time and step.

# For the time approach, it creates an input for every 3 seconds of the total acquisition 
# time. This duration is chosen because the step counter needs approximately 1.5 seconds 
# to predict a step, and for a stride (2 steps), we need 3 seconds.

# For the step approach, if a stride (2 steps) is detected within the 3-second window, 
# only the data between each stride (i.e., stride duration) is considered.

# The function creates a folder named 'data_cut' containing the .txt files, where each 
# file represents the input for the feature extractor stage implemented in a C++ code.

# Input:
#     fich (str): Name of the file containing the concatenated, interpolated, and sorted sensor data.

# Output:
#     None


Now create input for cpp ,the separation by step or time is made in the cpp code

"""



def separted_data_by_seconde_or_step(fich):
    print(f'Begin cut by step or time for {fich}')
    name=fich.split('/')[-1]
    
    if not os.path.exists(f'../data_treat/data_cut'):
            os.makedirs(f'../data_treat/data_cut')
    
    

    data=pd.read_csv(f'{fich}')
    
    data.to_csv(f'../data_treat/data_cut/{name.split(".")[0]}_cut.txt',index=False,header=False)
    
"""
================================================================================
Step 6: Create the BAT File to Launch the Feature Extraction with the C++ Files
================================================================================

Function: create_bat_file_for_feature_extraction

The feature extraction stage is performed by a C++ code, so we need to create a 
BAT file to launch it. This BAT file should consider all the data inputs created 
from the previous steps according to their file names.

Input:
    None
    
Output:
    None
"""

def create_bat(seuil_time,seuil_step):
    """
    @brief This function creates a BAT file to launch the feature extraction with the C++ files.
  
    @return None
    """
    print('Creating the BAT file')
    
    
    
    # Remove the existing directory if it exists
    if os.path.exists('cpp/data_to_put_in_cpp'):
        shutil.rmtree('cpp/data_to_put_in_cpp')
    
    # Copy the directory with data to the C++ directory
    shutil.copytree('../data_treat/data_cut', 'cpp/data_to_put_in_cpp')
    
    # List all files in the copied directory
    fichier = os.listdir('cpp/data_to_put_in_cpp')
    
    # Create and write to the BAT file
    with open("cpp/bat_all.bat", "w") as f:
        f.write("@echo off")
        f.write(f"{os.linesep}")
        f.write('g++ -o mon_executable main.cpp Sensors.cpp FeaturesCalculator.cpp Features.cpp')
        f.write(f"{os.linesep}")
        
        # Add commands to run the executable for each data file
        for fich in fichier:
            nom_output = f"{fich[0:-4]}.txt"
            f.write(f"mon_executable data_to_put_in_cpp/{fich} output_cpp/{nom_output} {seuil_time} {seuil_step}")
            f.write(f"{os.linesep}")

    print('BAT file created')
    


"""
================================================================================
Step 7: Launch the BAT File for Feature Extraction
================================================================================

Function: launch_bat_file_for_feature_extraction

Now we can launch the feature extraction stage, which is implemented by a C++ code, 
using this function.

Input:
    None
    
Output:
    None
"""

def launch_bat_file():
    
    """
    @brief This function launches the BAT file for feature extraction.
   
    @return None
    """
    print('Initiating feature extraction, a command console will open. Please close it to continue.')
    
    # Remove existing output directory if it exists
    if os.path.exists('cpp/output_cpp'):
        shutil.rmtree('cpp/output_cpp')
        
    os.makedirs('cpp/output_cpp')
    
    # Commands to run the BAT file
    commands_to_run = [
        'cd cpp',
        'bat_all'
    ]
    
    # Concatenate commands
    commands_concatenated = ' && '.join(commands_to_run)
    
    # Create command to start a new command prompt and run the concatenated commands
    cmd_command = f'start cmd /k "{commands_concatenated}"'
    
    # Start the process
    import time
    process = subprocess.Popen(cmd_command, shell=True)
    
    while process.poll() is None:
        time.sleep(1)  # Attendre 1 seconde
        

def launch_bat_file_test():
    
    """
    @brief This function launches the BAT file for feature extraction.
   
    @return None
    """
    print('Initiating feature extraction, a command console will open. Please close it to continue.')
    
    # Remove existing output directory if it exists
    if os.path.exists('cpp/output_cpp'):
        shutil.rmtree('cpp/output_cpp')
        
    os.makedirs('cpp/output_cpp')
    
    # Commands to run the BAT file
    commands_to_run = [
        'cd cpp',
        'bat_all'
    ]
    
    # Concatenate commands
    commands_concatenated = ' && '.join(commands_to_run)
    
    # Create command to start a new command prompt and run the concatenated commands
    cmd_command = f'start cmd /k "{commands_concatenated}"'
    
    # Start the process
    import time
    process = subprocess.Popen(cmd_command, shell=True)
    
    while process.poll() is None:
        time.sleep(1)  # Attendre 1 seconde
        
       
"""
================================================================================
Step 8: Concatenate the Output of the Feature Extraction Stage
================================================================================

Function: concatenate_feature_extraction_output

This function concatenates all the files created by the C++ code during the feature 
extraction stage into one unique dataframe file.

Input:
    show (boolean): Indicates whether to save the histograms of the features.

Output:
    None
"""

def concatenate_output_cpp(show=False):
    """
    Concatenates the output of the feature extraction stage into one unique dataframe file.

    @param show: If True, generates histograms for each feature.
    @type show: bool
    """
    files = os.listdir('cpp/output_cpp')
    df_list = []

    # Read each file and append its data to a list
    for file in files:
        data = pd.read_csv(f'cpp/output_cpp/{file}', delimiter=';')
    # if len(data) > 30:
    #     data = data.iloc[10:-10, :]  # Remove first and last 10 rows
    #     df_list.append(data)
        
        if len(data) > 0:
            # data = data.iloc[10:-10, :]  # Remove first and last 10 rows
            df_list.append(data)

    # Concatenate all dataframes in the list
    df = pd.concat(df_list, ignore_index=True)
    df.columns = df.columns.str.strip().str.replace(' +', ' ')
    # Save the concatenated dataframe to a CSV file
    df.to_csv('../data_treat/df_output_cpp_concatenate.csv', header=True, index=False)
    # df.to_csv('../data_treat/df_output_cpp_concatenate_excel.csv', header=True, index=False,sep=";",decimal=".")
    # Generate histograms if specified
    if show:
        # Labels for different modes
        labels = ['stair', 'escalator', 'elevator', 'still', 'walk']
        
        # Features to generate histograms for
        features = df.columns[1:]

        # Determine the minimum size of data for each mode
        mini_size = min(df[df['mode'] == label].shape[0] for label in labels)
        
        # Iterate over each feature to generate histograms
        for col in features:
            fig, axs = plt.subplots(5, 1, figsize=(10, 15))
            fig.suptitle(f'Histograms for {col}', fontsize=16)
            border = 1  # Adjust this value as per your preference
            x_min = df[col].min() - df[col].min() * 0.5
            x_max = df[col].max() + df[col].max() * 0.5
            
            # Generate histogram for each mode
            for j, label in enumerate(labels):
                df_mode = df[df['mode'] == label].sample(mini_size)
                hist, bins = np.histogram(df_mode[col].values, bins=30)
                y_max = hist.max()

                axs[j].hist(df_mode[col].values, bins=30, label=label, alpha=0.7)
                axs[j].set_title(f'Mode: {label}')
                axs[j].set_xlabel(col)
                axs[j].set_ylabel('Frequency')
                axs[j].legend()
                axs[j].set_xlim(x_min, x_max)
                axs[j].set_ylim(0, y_max)
                
            # Save the histogram figure
            if not os.path.exists(f'../data_treat/graphics_feature'):
                os.makedirs(f'../data_treat/graphics_feature')

            plt.tight_layout(rect=[0, 0, 1, 0.96])
            plt.savefig(f'../data_treat/graphics_feature/{col}.png')
            plt.show()





"""
================================================================================
Step 10: Classifier 5 class
================================================================================

Function: train_classifier_models

We considered 5 class : Elevator,Escalator,Stair,Still,Walk

Now we can train a few machine learning models using our data:

1. Decision Tree
2. XGBoost
3. Deep Neural Network (DNN)

Input:
    None

Output:
    Trained models for Decision Tree, XGBoost, and DNN
    
"""


def inputs_classifier(elements):
    """
    @brief Make the input for the classification with 5 classes when the floor changes
    
    0 : Elevator
    1 : Escalator
    2 : Stair
    3 : Still
    4 : Walk
    
    @return X_train: raw data to be trained in a classifier
    @rtype X_train: numpy.ndarray
    @return y_train: labels associated with the raw data trained in the classifier
    @rtype y_train: numpy.ndarray
    @return X_val: validation raw data of the classifier
    @rtype X_val: numpy.ndarray
    @return y_val: labels of the validation raw data
    @rtype y_val: numpy.ndarray
    @return X_test: raw data to test the classifier after the training
    @rtype X_test: numpy.ndarray
    @return y_test: labels of the test data
    @rtype y_test: numpy.ndarray
    """
    
    # Get the data that is the concatenated output of the cpp stage
    data = pd.read_csv('../data_treat/df_output_cpp_concatenate.csv')
    
    # Sort the data by mode
    data = data.sort_values(by='mode')
    
    # Function that labels the data by a number specific for each mode
    def map_mode_classif(mode):
        if mode == 'elevator':
            return 0
        elif mode == 'escalator':
            return 1
        elif mode == 'stair':
            return 2
        elif mode == 'still':
            return 3
        elif mode == 'walk':
            return 4
        else:
            return None
    
    # Create a new column in the data with the numeric label for each mode
    data['mode_numero'] = data['mode'].apply(lambda x: map_mode_classif(x))
    data = data.dropna(subset=['mode_numero'])
    
    # Align the columns of the data in the specific order

    
    
    
    data = data[elements]
    
    data=data.dropna()
    
    mode_u=np.unique(data['mode'].values)
        
    
    # Get the labels for each data point
    y = data['mode_numero'].values
    
    # Get the raw data without the labels
    X = data.drop(columns=['mode', 'mode_numero']).values
    
    # Split the data into sub-datasets
    X_train_temp, X_test, y_train_temp, y_test = train_test_split(
        X, y, test_size = 0.2, random_state = 42
    )

    X_train, X_val, y_train, y_val = train_test_split(
        X_train_temp, y_train_temp, test_size = 0.2, random_state = 42
    )
    
    
    
    # X_train, y_train = balance_data(X_train, y_train)
    u, c = np.unique(y_train, return_counts = True)
    print(u, c)
    
    feature=data.drop(columns=['mode', 'mode_numero']).columns
    dict_label_numero={'0':'elevator','1':'escalator','2':'stair','3':'still','4':'walk','6':'unknown'}
    return X_train, X_val, y_train, y_val, X_test, y_test, X, y,feature,dict_label_numero



def inputs_classifier_stair_walk(elements):
    """
    @brief Make the input for the classification with 5 classes when the floor changes
    
    0 : Elevator
    1 : Escalator
    2 : Stair
    3 : Still
    4 : Walk
    
    @return X_train: raw data to be trained in a classifier
    @rtype X_train: numpy.ndarray
    @return y_train: labels associated with the raw data trained in the classifier
    @rtype y_train: numpy.ndarray
    @return X_val: validation raw data of the classifier
    @rtype X_val: numpy.ndarray
    @return y_val: labels of the validation raw data
    @rtype y_val: numpy.ndarray
    @return X_test: raw data to test the classifier after the training
    @rtype X_test: numpy.ndarray
    @return y_test: labels of the test data
    @rtype y_test: numpy.ndarray
    """
    
    # Get the data that is the concatenated output of the cpp stage
    data = pd.read_csv('../data_treat/df_output_cpp_concatenate.csv')
    
    # Sort the data by mode
    data = data.sort_values(by='mode')
    
    # Function that labels the data by a number specific for each mode
    def map_mode_classif(mode):
        if mode == 'stair':
            return 0
        elif mode == 'walk':
            return 1
        else:
            return None
    
    # Create a new column in the data with the numeric label for each mode
    data['mode_numero'] = data['mode'].apply(lambda x: map_mode_classif(x))
    data = data.dropna(subset=['mode_numero'])
    

    
    
    data = data[elements]
    
    data=data.dropna()
    
    mode_u=np.unique(data['mode'].values)
        
    
    # Get the labels for each data point
    y = data['mode_numero'].values
    
    # Get the raw data without the labels
    X = data.drop(columns=['mode', 'mode_numero']).values
    
    # Split the data into sub-datasets
    X_train_temp, X_test, y_train_temp, y_test = train_test_split(
        X, y, test_size = 0.2, random_state = 42
    )

    X_train, X_val, y_train, y_val = train_test_split(
        X_train_temp, y_train_temp, test_size = 0.2, random_state = 42
    )
    
    
    
    # X_train, y_train = balance_data(X_train, y_train)
    u, c = np.unique(y_train, return_counts = True)
    print(u, c)
    
    feature=data.drop(columns=['mode', 'mode_numero']).columns
    dict_label_numero={'0':'elevator','1':'escalator','2':'stair','3':'still','4':'walk','6':'unknown'}
    return X_train, X_val, y_train, y_val, X_test, y_test, X, y,feature,dict_label_numero



"XGboost"
  
def xgboost(elements):
    """
    @brief Classifier Xgboost for 5 class
    
    """

    X_train, X_val, y_train, y_val, X_test, y_test, X, y,_,_=inputs_classifier(elements)

    max_depths = [3, 5, 7]
    learning_rates = [0.05, 0.1, 0.15, 0.01]
    n_estimators_list = [50, 100, 150, 200, 300]
    
    max_depths = [5, 7]
    learning_rates = [0.1, 0.15]
    n_estimators_list = [ 200, 300]
    
    max_depths = [7]
    learning_rates = [ 0.15]
    n_estimators_list = [300]
    
    best_accuracy = 0.0
    best_model = None
    best_params = None
    
    for depth in max_depths:
        for lr in learning_rates:
            for n_esti in n_estimators_list:
                clf_xgb = XGBClassifier(max_depth=depth, learning_rate=lr, n_estimators=n_esti,
                                        min_child_weight=1, gamma=1).fit(X_train, y_train)
            
                y_pred = clf_xgb.predict(X_test)
                accuracy = accuracy_score(y_test, y_pred)
            
                print(f"Accuracy: {accuracy:.2f}  {depth} {lr}  {n_esti}")
                
                if accuracy > best_accuracy:
                    best_accuracy = accuracy
                    best_model = clf_xgb
                    best_params = {'max_depth': depth, 'learning_rate': lr, 'n_estimators': n_esti}
    
    print("Best parameters:", best_params)
    print("Best accuracy:", best_accuracy)
    print(rf'{os.linesep}')
    y_pred = best_model.predict(X_test)
    
    # Calculate F1-score
    f_score = f1_score(y_test, y_pred,average='weighted')
    print("F_score ",f_score)
    
    # Calculate Confusion Matrix
    conf_matrix = confusion_matrix(y_test, y_pred)
    print(f"Conf Matrix {os.linesep}", conf_matrix)
    
    onnx_model_path = f"../data_treat/result_classifier/model/activity.onnx"
    
    initial_type = [('float_input', FloatTensorType([None,X_train.shape[1]]))]
    
    onnx_model = onnxmltools.convert.convert_xgboost(best_model, initial_types=initial_type, target_opset=8)
    onnx.save(onnx_model, onnx_model_path)
    


    
def dnn(elements):
    """
    @brief Classifier Dense Neuron Network for 5 classes
    """
    # pip install tensorflow==2.15.0 tf2onnx==1.16.1 keras==2.15.0

    # Get the training, validation, and test data
    X_train, X_val, y_train, y_val, X_test, y_test, X, y,_,_ = inputs_classifier(elements)

    # Define the input layer
    inpute = Input(shape=(X_train.shape[1], 1))

    conv5 = Conv1D(100, 3, padding='valid', activation='relu')(inpute)
    
    flatten = Flatten()(conv5)
    
    batch_nor = BatchNormalization()(flatten)
    
    dense1 = Dense(500, activation='relu')(batch_nor)
    dense2 = Dense(100, activation='relu')(dense1)
    dense3 = Dense(50, activation='relu')(dense2)
    
    # dropout=Dropout(0.5)(dense3)
    batch_nor2 = BatchNormalization()(dense3)
    
    dense4 = Dense(50, activation='relu')(batch_nor2)
    dense5 = Dense(20, activation='relu')(dense4)
    dense6 = Dense(10, activation='relu')(dense5)
    
    
    # dropout2=Dropout(0.5)(dense6)
    batch_nor3 = BatchNormalization()(dense6)
    
    # Define the output layer with softmax activation for classification
    output = Dense(5, activation='softmax')(batch_nor3)
    
    
    # Create the model
    model = Model(inputs=inpute, outputs=output)
    
    # Define the checkpoint to save the best model during training
    checkpoint = ModelCheckpoint(
        "../data_treat/result_classifier/model/dnn_inter_model.keras", 
        monitor='val_accuracy', save_best_only=True, mode='max', verbose=1
    )
    
    # Compile the model with SGD optimizer and sparse categorical crossentropy loss
    model.compile(optimizer=SGD(learning_rate=0.1), loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    
    def scheduler(epoch, lr):
        # Exemple simple : divise le learning rate par 10 tous les 10 epochs
        if epoch % 20 == 0 and epoch != 0:
            return lr * 0.1
        return lr

    adjust_lr=keras.callbacks.LearningRateScheduler(scheduler)
    
    # Reduce the learning rate when the validation accuracy stops improving
    reduce_lr = ReduceLROnPlateau(monitor='accuracy', factor=0.1, patience=3)

    # Train the model
    history = model.fit(
        X_train, y_train,
        epochs=20, batch_size=250,
        validation_data=(X_val, y_val),
        callbacks=[checkpoint,adjust_lr],
        verbose=1
    )
    
    # Load the best model saved during training
    best_model = load_model("../data_treat/result_classifier/model/dnn_inter_model.keras")
    
    
    y_pred_probs = best_model.predict(X_test)
    y_pred = np.argmax(y_pred_probs, axis=1)
    accuracy = accuracy_score(y_test, y_pred)
    print(rf'{os.linesep}')
    print(rf'{os.linesep}')
    print('accuracy ',accuracy)
    # Calculate F1-score
    f1 = f1_score(y_test, y_pred, average='weighted')
    print(f"Weighted F1-score: {f1}")

    # Calculate confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    print("Confusion Matrix:")
    print(cm)
    
    
    # Convert the Keras model to ONNX format
    onnx_model, _ = tf2onnx.convert.from_keras(best_model, opset=11)
    
    
    # Save the ONNX model
    with open("../data_treat/result_classifier/model/activitydnn.onnx", "wb") as f:
        f.write(onnx_model.SerializeToString())



def SVM(elements):
    X_train, X_val, y_train, y_val, X_test, y_test, X, y,_,_ = inputs_classifier(elements)
    
    
    k= ['rbf', 'linear']
    c=  [0.1, 1, 10, 100]
    g= ['scale', 'auto']
    
    best_accuracy=0
    
    best_svm=None
    for g1 in g:
        for k1 in k:
            for c1 in c:
                svm = SVC(decision_function_shape='ovr', kernel=k1, C=c1, gamma=g1, random_state=42)
                svm.fit(X_train, y_train)
            
                y_pred = svm.predict(X_test)
                
                print("Accuracy:", accuracy_score(y_test, y_pred))
                if accuracy_score(y_test, y_pred)>best_accuracy:
                    best_accuracy=accuracy_score(y_test, y_pred)
                    best_svm=svm

    
    initial_type = [('float_input', FloatTensorType([None, X_train.shape[1]]))]
    onnx_model = convert_sklearn(best_svm, initial_types=initial_type)
    
    # Sauvegarder le modèle ONNX
    with open("../data_treat/result_classifier/model/svm_model.onnx", "wb") as f:
        f.write(onnx_model.SerializeToString())
    


if __name__ == '__main__':
    print('DEBUT')
    print(rf'{os.linesep}')
    
    
    if os.path.exists('../data_treat'):
        print(rf'Remove data treat')
        shutil.rmtree('../data_treat')
        print(rf'{os.linesep}')
    if os.path.exists('cpp/output_cpp'):
        print(rf'Remove output_cpp')
        shutil.rmtree('cpp/output_cpp')
        print(rf'{os.linesep}')
    
    print(rf'{os.linesep}')
    fichiers = os.listdir('../data_original/zip')

    for fich in fichiers:
        if fich.endswith('.zip'):
            print(f'The file {fich} has been unzipped')
            unzip_file(fich)
            
    fichiers = os.listdir('../data_treat/unzip')
    
    print(rf'{os.linesep}')

    for fich in fichiers:
        print(f'Begin rename {fich}')
        rename_original_data(fich)
    
    
    print(rf'{os.linesep}')
    fichiers=os.listdir('../data_treat/rename')
    
    for folder in fichiers:
        print(rf'Begin to interpolate {folder}')
        interpolation_of_data_rename(f'{folder}')
    
    print(rf'{os.linesep}')
    
    fichiers=os.listdir('../data_treat/data_interpolate_base')
    
    # input_visu_data = input(prompt='Do you want to see the data Y/N -> ')

    # if input_visu_data.lower() == 'y':
    #     for fich in fichiers:
    #         visu_data(f'../data_treat/data_interpolate_base/{fich}', fich)
    
        
    sort_data_by_step()
    
    
    # input_visu_data_sort=input('Do you want to see the data sorted Y/N -> ')
    
        
    # if input_visu_data_sort.lower()=='y':
    
    #     fichiers=os.listdir('../data_treat/data_interpolate_sorted')
        
    #     for fich in fichiers:
    #         visu_data_sorted(f'../data_treat/data_interpolate_sorted/{fich}',fich)
            
            
    fichiers=os.listdir('../data_treat/data_interpolate_sorted')
    print(rf'{os.linesep}')
    
    for fich in fichiers:
        separted_data_by_seconde_or_step(f'../data_treat/data_interpolate_sorted/{fich}')
            
    print(rf'{os.linesep}')
    
    seuil_time=3
    seuil_step=3
    
    create_bat(seuil_time,seuil_step)
    print(rf'{os.linesep}')
    
    launch_bat_file()
    
    print(rf'{os.linesep}')
    
    
    input_bat=input("Write ok when the cmd is over -> ")
    
    while input_bat.lower()!='ok':
        input_bat=input("Write ok when the cmd is over")
    
    print(rf'{os.linesep}')
    print('Concatenation des fichier de output cpp')
    
    print('visualisation histogramm feature')
    show=False
    
    try:
        input_feature=inputimeout(prompt='Do you want to see the feature data Y/N -> ',timeout=1)
    except:
        input_feature='n'
    
    if input_feature.lower()=='y':
        show=True
    else:
        show=False
    show=False
    print('Concatenation')

    show=False    
    concatenate_output_cpp(show)
    
    print(rf'{os.linesep}')
    if os.path.exists(f'../data_treat/data_output_cpp'):
        shutil.rmtree(f'../data_treat/data_output_cpp')
        
        
    shutil.copytree(f'cpp/output_cpp', f'../data_treat/data_output_cpp')
    
    if not os.path.exists(f'../data_treat/result_classifier/model'):
        os.makedirs(f'../data_treat/result_classifier/model')
    
    elements = [
        # "acc_arc", "gyr_arc", "mag_arc", 
        # "acc_x_aad", "acc_x_mean", "acc_x_std", "acc_x_kurt", "acc_x_skew",
        # "acc_y_aad", "acc_y_mean", "acc_y_std", "acc_y_kurt", "acc_y_skew",
        "acc_z_aad", "acc_z_mean", "acc_z_std", "acc_z_kurt", "acc_z_skew",
        # "gyr_x_aad", "gyr_x_mean", "gyr_x_std", "gyr_x_kurt", "gyr_x_skew",
        # "gyr_y_aad", "gyr_y_mean", "gyr_y_std", "gyr_y_kurt", "gyr_y_skew",
        "gyr_z_aad", "gyr_z_mean", "gyr_z_std", "gyr_z_kurt", "gyr_z_skew",
        # "mag_x_aad", "mag_x_mean", "mag_x_std", "mag_x_kurt", "mag_x_skew",
        # "mag_y_aad", "mag_y_mean", "mag_y_std", "mag_y_kurt", "mag_y_skew",
        "mag_z_aad", "mag_z_mean", "mag_z_std", "mag_z_kurt", "mag_z_skew",
        "baro_aad", "baro_mean", "baro_std", "baro_kurt", "baro_skew",
        "nb_step",
          "aad_acc_norm", "mean_acc_norm", "std_acc_norm", "kurt_acc_norm", "skew_acc_norm",
          "aad_gyro_norm", "mean_gyro_norm", "std_gyro_norm", "kurtosis_gyro_norm", "skewness_gyro_norm",
            "aad_mag_norm", "mean_mag_norm", "std_mag_norm", "kurt_mag_norm", "skew_mag_norm",  
    "time_diff",
    "mode", "mode_numero"
      ]
    
    with open("list_features.txt", 'w', encoding='utf-8') as file:
        for string in elements:
            file.write(string + '\n')
            
        file.write(seuil_time + '\n')
        file.write(seuil_step + '\n')
            
    
    
    print(rf'{os.linesep}')
    print(elements)
    print(rf'{os.linesep}')
    print('Begin XGboost')
    xgboost(elements)

    
    print(rf'{os.linesep}')
    print('Begin dnn')
    dnn(elements)
    
    
    
    
    accuracy_test=def_test.test_all(seuil_time, seuil_step, elements)
    
    n='{0:.6g}'.format(accuracy_test)
    
    number='test_'+str(n)+f'_{seuil_time}_{seuil_step}'
    
    base=f'../test_accuracy/{number}'
    if not os.path.exists(base):
        os.makedirs(base)
        shutil.copy2(f'__main.py', f'{base}/__main.py')
        shutil.copy2(f"list_features.txt", f'{base}/list_features.txt')
        shutil.copy(f'../data_treat/result_classifier/model/activity.onnx',f'{base}/activity.onnx')
        shutil.copy(f'../data_treat/result_classifier/model/activitydnn.onnx',f'{base}/activitydnn.onnx')
        
    
    
            