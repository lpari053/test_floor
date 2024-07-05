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
    
    
    df=pd.concat([data_acc,data_gyr,data_mag,data_baro],axis=1)  
    df = df.loc[:, ~df.columns.duplicated()]
    
    new_order = ['mode','acc_x','acc_y','acc_z','gyr_x','gyr_y','gyr_z','mag_x','mag_y','mag_z','pressure','time','nb_step']
    df=df[new_order]
    if not os.path.exists(f'../data_treat/data_interpolate_test'):
        os.makedirs(f'../data_treat/data_interpolate_test') 
    df.to_csv(f'../data_treat/data_interpolate_test/{folder}.txt',header=True,index=False)  
    


def separted_data_by_seconde_or_step(fich):
    print(f'Begin cut by step or time for {fich}')
    name=fich.split('/')[-1]
    
    if not os.path.exists(f'../data_treat/data_cut_test'):
            os.makedirs(f'../data_treat/data_cut_test')
    
    

    data=pd.read_csv(f'{fich}')
    
    data['time']=data['time']-data['time'][0]
    
    
    data.to_csv(f'../data_treat/data_cut_test/{name.split(".")[0]}_cut.txt',index=False,header=False)
    
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
    if os.path.exists('cpp_test/data_to_put_in_cpp'):
        shutil.rmtree('cpp_test/data_to_put_in_cpp')
    
    # Copy the directory with data to the C++ directory
    shutil.copytree('../data_treat/data_cut_test', 'cpp_test/data_to_put_in_cpp')
    
    # List all files in the copied directory
    fichier = os.listdir('cpp_test/data_to_put_in_cpp')
    
    # Create and write to the BAT file
    with open("cpp_test/bat_all.bat", "w") as f:
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
    if os.path.exists('cpp_test/output_cpp'):
        shutil.rmtree('cpp_test/output_cpp')
        
    os.makedirs('cpp_test/output_cpp')
    
    # Commands to run the BAT file
    commands_to_run = [
        'cd cpp_test',
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
        time.sleep(50)  
        



def prediction(elements):
    import onnxruntime as ort
    session_dnn = ort.InferenceSession('../data_treat/result_classifier/model/activitydnn.onnx')
    
    for fich in os.listdir("../data_treat/data_output_cpp_test"):
        data=pd.read_csv(rf'../data_treat/data_output_cpp_test/{fich}',sep=';')
        data.columns = data.columns.str.strip().str.replace(' +', ' ')
        data2=data.copy()
        data_2=data2[elements]
        
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
                return np.nan
        
        # Create a new column in the data with the numeric label for each mode
        data['mode_numero'] = data['mode'].apply(lambda x: map_mode_classif(x))
        
        y=data['mode_numero'].values
        time_debut=data['time_debut'].values
        time_fin=data['time_fin'].values
        
    
        
        if len(data)>1:
            
            data_input=data[elements]
            X=data_input.values
            
            pred=[]
            true=[]
            
            pred2=[]
            true2=[]
            
            for i in range(0,len(data_input)):
                
                input_data = X[i].astype(np.float32).reshape(1,X[i].shape[0],1)

                input_name = session_dnn.get_inputs()[0].name
                outputs = np.argmax(session_dnn.run(None, {input_name: input_data})[0][0])
                
                if y[i]!=np.nan:
                    pred2.append(outputs)
                    true2.append(y[i])
                
                pred.append(outputs)
                true.append(y[i])
                
            # visu_data_pred(fich,time_debut,time_fin,pred,true)
            
    print('Accuracy _test: ',accuracy_score(true2,pred2))
    
    return accuracy_score(true2,pred2)
                

    
def visu_data_pred(fich,time_debut,time_fin,pred,true):
    
    
    color_to_integer = {
    "0": "blue",
    "1": "red",
    "2": "green",
    "3": "yellow",
    "4": "violet",
    "5":"white"
}
        
    couleurs_l = {
     "elevator": "blue",
     "escalator": "red",
     "stair": "green",
     "still": "yellow",
     "walk": "violet",
     "unknown": "white"
}



   
    data_original=pd.read_csv(f'../data_treat/data_cut_test/{fich}')
    data_original.columns= ['mode','acc_x','acc_y','acc_z','gyr_x','gyr_y','gyr_z','mag_x','mag_y',
                            'mag_z','pressure','time','nb_step']
    
    data_original['time']=data_original['time']-data_original['time'][0]
    
    max_acc_x = data_original['acc_x'].max()+1
    max_acc_y = data_original['acc_y'].max()+1
    max_acc_z = data_original['acc_z'].max()+1
    
    max_gyr_x = data_original['gyr_x'].max()+1
    max_gyr_y = data_original['gyr_y'].max()+1
    max_gyr_z = data_original['gyr_z'].max()+1
    
    max_mag_x = data_original['mag_x'].max()+1
    max_mag_y = data_original['mag_y'].max()+1
    max_mag_z = data_original['mag_z'].max()+1
    
    min_acc_x = data_original['acc_x'].min()-1
    min_acc_y = data_original['acc_y'].min()-1
    min_acc_z = data_original['acc_z'].min()-1
    
    min_gyr_x = data_original['gyr_x'].min()-1
    min_gyr_y = data_original['gyr_y'].min()-1
    min_gyr_z = data_original['gyr_z'].min()-1
    
    min_mag_x = data_original['mag_x'].min()-1
    min_mag_y = data_original['mag_y'].min()-1
    min_mag_z = data_original['mag_z'].min()-1
    
    nom_dossier = fich
    
    #Getting the name , mode and people of the data to make the name and title of the plot
    parties = nom_dossier.split('_')
    if parties[0]=='no':
        parties=['no_name',parties[2],parties[3]]
    personne = parties[0]
    date = parties[1]
    type_activite =parties[2] 
    print(rf'{os.linesep}')
    print("Chemin:", fich)
    print("Personne:", personne)
    print("Date:", date)
    print(rf'{os.linesep}')
    
    titre=fr"{type_activite.upper()} Date : {date}  Personne : {personne}"
    
    data_baro=data_original[['mode','time','pressure']]
    data_acc=data_original[['mode','time','acc_x','acc_y','acc_z','nb_step']]
    data_gyr=data_original[['mode','time','gyr_x','gyr_y','gyr_z']]
    data_mag=data_original[['mode','time','mag_x','mag_y','mag_z']]
    
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
    
    
    

    
    
    for row in axs:
        for ax in row:
            for i in range(0,len(time_debut)):
                # ax.axvline(x=time_debut[i], color='g', linestyle='--', label='Ligne verticale')
                # ax.axvline(x=time_fin[i], color='g', linestyle='--', label='Ligne verticale')
                ax.axvspan(time_debut[i], time_fin[i],ymin=0, ymax=0.5,color=color_to_integer.get(str(pred[i]), 'gray'), alpha=0.3, label='Zone colorée')
                ax.axvspan(time_debut[i], time_fin[i],ymin=0.5, ymax=1,color=color_to_integer.get(str(true[i]), 'gray'), alpha=0.3, label='Zone colorée')
      
                
    fig.text(0.8, 0.05, 'y_pred: bas\ny_true: haut', va='center', ha='center', fontsize=12, bbox=dict(facecolor='lightgray', alpha=0.5, pad=10))


    
    import matplotlib.patches as mpatches 
    legend_patches = [mpatches.Patch(color=color, label=label) for label, color in couleurs_l.items()]
    plt.legend(handles=legend_patches, loc='upper left', bbox_to_anchor=(1, 1))
    
    

    plt.suptitle(titre)
    plt.tight_layout()
    
    if not os.path.exists('../graphics_pred'):
        os.makedirs('../graphics_pred')
    
    number=len(os.listdir('../graphics_pred/'))
    
    
    
    plt.savefig(rf'../graphics_pred/{number}.PNG')
    plt.show()
    

def test_all(seuil_time,seuil_step,elements):
    
    elements.pop()
    elements.pop()
    
    print(rf'{os.linesep}')
    print('DEBUT TEST')
    print(rf'{os.linesep}')
    
    
    if os.path.exists('cpp_test/output_cpp'):
        print(rf'Remove output_cpp')
        shutil.rmtree('cpp_test/output_cpp')
        print(rf'{os.linesep}')
    

    if os.path.exists('../data_treat/data_interpolate_test'):
        print(rf'Remove interpolate test')
        shutil.rmtree('../data_treat/data_interpolate_test')
        print(rf'{os.linesep}')
    
    
    print(rf'{os.linesep}')
    fichiers=os.listdir('../data_treat/rename')
    
    for folder in fichiers:
        print(rf'Begin to interpolate {folder}')
        interpolation_of_data_rename(f'{folder}')
    

            
    fichiers=os.listdir('../data_treat/data_interpolate_test')
    print(rf'{os.linesep}')
    
    for fich in fichiers:
        separted_data_by_seconde_or_step(f'../data_treat/data_interpolate_test/{fich}')
            
    print(rf'{os.linesep}')
    
    
    create_bat(seuil_time,seuil_step)
    print(rf'{os.linesep}')
    
    launch_bat_file()
    
    print(rf'{os.linesep}')
    
    ok=input("write ok when over :")

    if os.path.exists(f'../data_treat/data_output_cpp_test'):
        shutil.rmtree(f'../data_treat/data_output_cpp_test')
        
    shutil.copytree(f'cpp_test/output_cpp', f'../data_treat/data_output_cpp_test')
    prediction(elements)
    



    
    