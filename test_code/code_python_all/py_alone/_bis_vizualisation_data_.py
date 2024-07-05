import os
import warnings

import matplotlib.pyplot as plt  
import seaborn as sns 
import numpy as np
import pandas as pd

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
    data_acc=pd.read_csv(f'{chemin}/ACC.txt',header=0)
    data_gyr=pd.read_csv(f'{chemin}/GYR.txt',header=0)
    data_mag=pd.read_csv(f'{chemin}/MAG.txt',header=0)
    data_baro=pd.read_csv(f'{chemin}/BARO.txt',header=0)
    

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
    
    titre=fr"{type_activite.upper()} Date : {date}  Personne : {personne}"
    
        
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
    
    if not os.path.exists(f'../../data_treat/graphics/{str(type_activite)}/'):
            os.makedirs(f'../../data_treat/graphics/{str(type_activite)}/')
    
    plt.savefig(f'../../data_treat/graphics/{str(type_activite)}/{file}.png')
    plt.show()
    
    
    
fichiers=os.listdir('../../data_treat/data_interpolate_base')
for fich in fichiers:
    visu_data(f'../../data_treat/data_interpolate_base/{fich}', fich)
    