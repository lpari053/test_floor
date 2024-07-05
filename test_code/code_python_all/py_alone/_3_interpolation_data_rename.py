"""
================================================================================
File Name: _3_interpolation_data_rename.py
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

import matplotlib.pyplot as plt  
import seaborn as sns 
import numpy as np
import pandas as pd

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
    
    path=rf"../../data_treat/rename/{folder}"  #Root path where to find folder where whithin there is the data collect for each sensor considered
    
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
    r=modie.values
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
    
    
    data_acc=data_acc.loc[data_acc['mode'] != 'unknown']
    data_gyr=data_gyr.loc[data_gyr['mode'] != 'unknown']
    data_mag=data_mag.loc[data_mag['mode'] != 'unknown']
    data_baro=data_baro.loc[data_baro['mode'] != 'unknown']
    
    #reindexing on the same base the dataframe for each sensor
    data_acc.reset_index(drop=True, inplace=True)
    data_mag.reset_index(drop=True, inplace=True)
    data_baro.reset_index(drop=True, inplace=True)
    data_gyr.reset_index(drop=True, inplace=True)
    
    #Re-extract the activity considered fo each time of acquisition
    mode=np.array(data_acc.iloc[:,0])
    
    #Search the index where the activity change considered the previous activity
    indices_changement_valeurs = []
    for i in range(1, len(mode)):
        if mode[i] != mode[i-1]:
            indices_changement_valeurs.append(i)
   

    
    #If for all the acquition there is only one activty considered save the data directly
    if len(indices_changement_valeurs)==0:
        mode=data_acc.iloc[0,0]
        if not os.path.exists(f'../data_treat/data_interpolate_base/{folder}_{mode}_0'):
            os.makedirs(f'../data_treat/data_interpolate_base/{folder}_{mode}_0') 
        
        data_acc.to_csv(f'../../data_treat/data_interpolate_base/{folder}_{mode}_0/ACC.txt',header=True,index=False)
        data_gyr.to_csv(f'../../data_treat/data_interpolate_base/{folder}_{mode}_0/GYR.txt',header=True,index=False)
        data_mag.to_csv(f'../../data_treat/data_interpolate_base/{folder}_{mode}_0/MAG.txt',header=True,index=False)
        data_baro.to_csv(f'../../data_treat/data_interpolate_base/{folder}_{mode}_0/BARO.txt',header=True,index=False)
             
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
            
            if not os.path.exists(f'../data_treat/data_interpolate_base/{folder}_{mode}_{i}'):
                os.makedirs(f'../data_treat/data_interpolate_base/{folder}_{mode}_{i}')     
                
                
            data_acc_inter.to_csv(f'../../data_treat/data_interpolate_base/{folder}_{mode}_{i}/ACC.txt',header=True,index=False)
            data_gyr_inter.to_csv(f'../../data_treat/data_interpolate_base/{folder}_{mode}_{i}/GYR.txt',header=True,index=False)
            data_mag_inter.to_csv(f'../../data_treat/data_interpolate_base/{folder}_{mode}_{i}/MAG.txt',header=True,index=False)
            data_baro_inter.to_csv(f'../../data_treat/data_interpolate_base/{folder}_{mode}_{i}/BARO.txt',header=True,index=False)
                 
            df=pd.concat([data_acc_inter,data_gyr_inter,data_mag_inter,data_baro_inter],axis=1)  
            df = df.loc[:, ~df.columns.duplicated()]
            
            new_order = ['mode','acc_x','acc_y','acc_z','gyr_x','gyr_y','gyr_z','mag_x','mag_y','mag_z','pressure','time','nb_step']
            df=df[new_order]
            if not os.path.exists(f'../data_treat/data_interpolate'):
                os.makedirs(f'../data_treat/data_interpolate') 
            df.to_csv(f'../data_treat/data_interpolate/{folder}_{mode}_{i}.txt',header=True,index=False)  
    
            
    return r
            
t=r"galaxy10_17062024-12-26-40-536"


r=interpolation_of_data_rename(t)
















