import os
import pandas as pd
import numpy as np
import glob
import matplotlib.pyplot as plt
import shutil
import subprocess

from keras.models import load_model

def create_bat_test():
    """
    @brief This function creates a BAT file to launch the feature extraction with the C++ files.
  
    @return None
    """
    print('Creating the BAT file')
    
    seuil_time=3
    seuil_step=2
    
    # Remove the existing directory if it exists
    if os.path.exists('../cpp_test/data_to_put_in_cpp'):
        shutil.rmtree('../cpp_test/data_to_put_in_cpp')
    
    # Copy the directory with data to the C++ directory
    shutil.copytree('../../data_treat/data_cut', '../cpp_test/data_to_put_in_cpp')
    
    # List all files in the copied directory
    fichier = os.listdir('../cpp_test/data_to_put_in_cpp')
    
    # Create and write to the BAT file
    with open("../cpp_test/bat_all.bat", "w") as f:
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

def launch_bat_file_test():
    
    """
    @brief This function launches the BAT file for feature extraction.
   
    @return None
    """
    print('Initiating feature extraction, a command console will open. Please close it to continue.')
    
    # Remove existing output directory if it exists
    if os.path.exists('../cpp_test/output_cpp'):
        shutil.rmtree('../cpp_test/output_cpp')
        
    os.makedirs('../cpp_test/output_cpp')
    
    # Commands to run the BAT file
    commands_to_run = [
        'cd ../cpp_test',
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
        time.sleep(20)  # Attendre 1 seconde


def prediction_dnn():
    
    with open('predictions.txt', 'w') as file:
        file.write(f"fich,pred,y,time_debut\n")
    
        fichiers=os.listdir('../cpp_test/output_cpp')
        
        model=load_model('../../data_treat/result_classifier/model/dnn_inter_model.keras')
        
        for fich in fichiers:
            print(fich)
            data=pd.read_csv(f'../cpp_test/output_cpp/{fich}',delimiter=";").dropna()
            data.columns = data.columns.str.strip().str.replace(' +', ' ')
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
            elements = ["time_debut",
                "acc_arc", "gyr_arc", "mag_arc", 
                "acc_x_aad", "acc_x_mean", "acc_x_std", "acc_x_kurt", "acc_x_skew",
                "acc_y_aad", "acc_y_mean", "acc_y_std", "acc_y_kurt", "acc_y_skew",
                "acc_z_aad", "acc_z_mean", "acc_z_std", "acc_z_kurt", "acc_z_skew",
                "gyr_x_aad", "gyr_x_mean", "gyr_x_std", "gyr_x_kurt", "gyr_x_skew",
                "gyr_y_aad", "gyr_y_mean", "gyr_y_std", "gyr_y_kurt", "gyr_y_skew",
                "gyr_z_aad", "gyr_z_mean", "gyr_z_std", "gyr_z_kurt", "gyr_z_skew",
                "mag_x_aad", "mag_x_mean", "mag_x_std", "mag_x_kurt", "mag_x_skew",
                "mag_y_aad", "mag_y_mean", "mag_y_std", "mag_y_kurt", "mag_y_skew",
                "mag_z_aad", "mag_z_mean", "mag_z_std", "mag_z_kurt", "mag_z_skew",
                "baro_aad", "baro_mean", "baro_std", "baro_kurt", "baro_skew",
                "nb_step", "baro_diffFirstLast", #"baro_pente",
                "aad_acc_norm", "mean_acc_norm", "std_acc_norm", "kurt_acc_norm", "skew_acc_norm",
                "aad_gyro_norm", "mean_gyro_norm", "std_gyro_norm", "kurtosis_gyro_norm", "skewness_gyro_norm",
                "aad_mag_norm", "mean_mag_norm", "std_mag_norm", "kurt_mag_norm", "skew_mag_norm", "time_diff", "mode", "mode_numero"
            ]
            data=data[elements]
            
            t=data['time_debut'].values
            
            Y = data['mode_numero'].values
            
            # Get the raw data without the labels
            X = data.drop(columns=['mode', 'mode_numero','time_debut'])
            
            
            for ligne in range(0,len(X)):
                
                x=X.iloc[ligne,:].values
                y=Y[ligne]
                
                pred=np.argmax(model.predict(x.reshape(1,-1),verbose=0))
                print(pred,y)
                
                file.write(f"{fich},{pred},{y},{t[ligne]}\n")
                
    file.close()

    

import onnxruntime as ort

def prediction_xg():
    
    with open('predictions_xg.txt', 'w') as file:
        file.write(f"fich,pred,y,time_debut\n")
    
        fichiers=os.listdir('../cpp_test/output_cpp')
        
        ort_session = ort.InferenceSession('../../data_treat/result_classifier/model/activity.onnx')
        
        for fich in fichiers:
            print(fich)
            data=pd.read_csv(f'../cpp_test/output_cpp/{fich}',delimiter=";").dropna()
            data.columns = data.columns.str.strip().str.replace(' +', ' ')
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
            elements = ["time_debut",
                "acc_arc", "gyr_arc", "mag_arc", 
                "acc_x_aad", "acc_x_mean", "acc_x_std", "acc_x_kurt", "acc_x_skew",
                "acc_y_aad", "acc_y_mean", "acc_y_std", "acc_y_kurt", "acc_y_skew",
                "acc_z_aad", "acc_z_mean", "acc_z_std", "acc_z_kurt", "acc_z_skew",
                "gyr_x_aad", "gyr_x_mean", "gyr_x_std", "gyr_x_kurt", "gyr_x_skew",
                "gyr_y_aad", "gyr_y_mean", "gyr_y_std", "gyr_y_kurt", "gyr_y_skew",
                "gyr_z_aad", "gyr_z_mean", "gyr_z_std", "gyr_z_kurt", "gyr_z_skew",
                "mag_x_aad", "mag_x_mean", "mag_x_std", "mag_x_kurt", "mag_x_skew",
                "mag_y_aad", "mag_y_mean", "mag_y_std", "mag_y_kurt", "mag_y_skew",
                "mag_z_aad", "mag_z_mean", "mag_z_std", "mag_z_kurt", "mag_z_skew",
                "baro_aad", "baro_mean", "baro_std", "baro_kurt", "baro_skew",
                "nb_step", "baro_diffFirstLast", #"baro_pente",
                "aad_acc_norm", "mean_acc_norm", "std_acc_norm", "kurt_acc_norm", "skew_acc_norm",
                "aad_gyro_norm", "mean_gyro_norm", "std_gyro_norm", "kurtosis_gyro_norm", "skewness_gyro_norm",
                "aad_mag_norm", "mean_mag_norm", "std_mag_norm", "kurt_mag_norm", "skew_mag_norm", "time_diff", "mode", "mode_numero"
            ]
            data=data[elements]
            
            t=data['time_debut'].values
            
            Y = data['mode_numero'].values
            
            # Get the raw data without the labels
            X = data.drop(columns=['mode', 'mode_numero','time_debut'])
            
            
            for ligne in range(0,len(X)):
                
                x=X.iloc[ligne,:].values
                y=Y[ligne]
                ort_inputs = {ort_session.get_inputs()[0].name: x.reshape(1, -1).astype(np.float32)}
                ort_outs = ort_session.run(None, ort_inputs)
                
                pred = ort_outs[0][0]
                # pred=np.argmax(model.predict(x.reshape(1,-1),verbose=0))
                print(pred,y)
                
                file.write(f"{fich},{pred},{y},{t[ligne]}\n")
                
    file.close()

def visu():
    
    data_pred=pd.read_csv('predictions.txt',delimiter=',')
    fichiers=data_pred['fich'].values
    couleurs = {
    "0": "blue",
    "1": "red",
    "2": "green",
    "3": "yellow",
    "4": "violet"
}
        
    couleurs_l = {
     "elevator": "blue",
     "escalator": "red",
     "stair": "green",
     "still": "yellow",
     "walk": "violet"
}
    
    # fichiers=os.listdir('../../data_treat/data_interpolate_base')
    fichiers=np.unique(fichiers)
    for fich2 in fichiers:
        donnee=data_pred[data_pred['fich']==fich2]
        
        highlight_time=donnee['time_debut'].values
        prediction=donnee['pred'].values
        fich=fich2.split('_sort_cut.txt')[0]
        
        
        chemin=f'../../data_treat/data_interpolate_base/{fich}'
    
        data_acc=pd.read_csv(f'{chemin}/ACC.txt',header=0)
        data_gyr=pd.read_csv(f'{chemin}/GYR.txt',header=0)
        data_mag=pd.read_csv(f'{chemin}/MAG.txt',header=0)
        data_baro=pd.read_csv(f'{chemin}/BARO.txt',header=0)
        
        data_acc.iloc[:,1]=data_acc.iloc[:,1]-data_acc.iloc[0,1]
        data_baro.iloc[:,1]=data_baro.iloc[:,1]-data_baro.iloc[0,1]
        data_gyr.iloc[:,1]=data_gyr.iloc[:,1]-data_gyr.iloc[0,1]
        data_mag.iloc[:,1]=data_mag.iloc[:,1]-data_mag.iloc[0,1]
        
        
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
        
        for ax in axs.flatten():
            for time, pred in zip(highlight_time, prediction):
                # Plot vertical lines
                ax.axvline(x=time, color='k', linestyle='--')
                
                # Plot shaded regions
            for idx in range(len(prediction) - 1):
                ax.axvspan(highlight_time[idx], highlight_time[idx + 1], facecolor=couleurs.get(str(prediction[idx]), 'gray'), alpha=0.4)
            
            ax.axvspan(highlight_time[-1], max(data_mag.iloc[:, 1]), facecolor=couleurs.get(str(prediction[-1]), 'gray'), alpha=0.4)
        
        
        
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
        
        import matplotlib.patches as mpatches 
        legend_patches = [mpatches.Patch(color=color, label=label) for label, color in couleurs_l.items()]
        plt.legend(handles=legend_patches, loc='upper left', bbox_to_anchor=(1, 1))

           
        
        mode=type_activite.split(".")[0]
        plt.suptitle(titre)
        plt.tight_layout()
        if not os.path.exists(f'../../data_treat/graphics_pred/dnn/{mode}'):
            os.makedirs(f'../../data_treat/graphics_pred/dnn/{mode}')
        plt.savefig(f'../../data_treat/graphics_pred/dnn/{mode}/{chemin.split("/")[-1]}.png')
        plt.show()
 
def visu_xg():
    
    data_pred=pd.read_csv('predictions_xg.txt',delimiter=',')
    fichiers=data_pred['fich'].values
    couleurs = {
    "0": "blue",
    "1": "red",
    "2": "green",
    "3": "yellow",
    "4": "violet"
}
        
    couleurs_l = {
     "elevator": "blue",
     "escalator": "red",
     "stair": "green",
     "still": "yellow",
     "walk": "violet"
}
    
    # fichiers=os.listdir('../../data_treat/data_interpolate_base')
    fichiers=np.unique(fichiers)
    for fich2 in fichiers:
        donnee=data_pred[data_pred['fich']==fich2]
        
        highlight_time=donnee['time_debut'].values
        prediction=donnee['pred'].values
        fich=fich2.split('_sort_cut.txt')[0]
        
        
        chemin=f'../../data_treat/data_interpolate_base/{fich}'
    
        data_acc=pd.read_csv(f'{chemin}/ACC.txt',header=0)
        data_gyr=pd.read_csv(f'{chemin}/GYR.txt',header=0)
        data_mag=pd.read_csv(f'{chemin}/MAG.txt',header=0)
        data_baro=pd.read_csv(f'{chemin}/BARO.txt',header=0)
        
        data_acc.iloc[:,1]=data_acc.iloc[:,1]-data_acc.iloc[0,1]
        data_baro.iloc[:,1]=data_baro.iloc[:,1]-data_baro.iloc[0,1]
        data_gyr.iloc[:,1]=data_gyr.iloc[:,1]-data_gyr.iloc[0,1]
        data_mag.iloc[:,1]=data_mag.iloc[:,1]-data_mag.iloc[0,1]
        
        
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
        
        for ax in axs.flatten():
            for time, pred in zip(highlight_time, prediction):
                # Plot vertical lines
                ax.axvline(x=time, color='k', linestyle='--')
                
                # Plot shaded regions
            for idx in range(len(prediction) - 1):
                ax.axvspan(highlight_time[idx], highlight_time[idx + 1], facecolor=couleurs.get(str(prediction[idx]), 'gray'), alpha=0.4)
            
            ax.axvspan(highlight_time[-1], max(data_mag.iloc[:, 1]), facecolor=couleurs.get(str(prediction[-1]), 'gray'), alpha=0.4)
        
        
        
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
        
        import matplotlib.patches as mpatches 
        legend_patches = [mpatches.Patch(color=color, label=label) for label, color in couleurs_l.items()]
        plt.legend(handles=legend_patches, loc='upper left', bbox_to_anchor=(1, 1))

           
        
        mode=type_activite.split(".")[0]
        plt.suptitle(titre)
        plt.tight_layout()
        if not os.path.exists(f'../../data_treat/graphics_pred/xg/{mode}'):
            os.makedirs(f'../../data_treat/graphics_pred/xg/{mode}')
        plt.savefig(f'../../data_treat/graphics_pred/xg/{mode}/{chemin.split("/")[-1]}.png')
        plt.show()
if __name__ == '__main__':
    create_bat_test()
    launch_bat_file_test()
    prediction_dnn()
    visu()
    prediction_xg()
    visu_xg()
           