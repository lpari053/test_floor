"""
================================================================================
File Name: _4_sort_data.py
Author: PARISOT Laura
Creation Date: 26/05/2024

================================================================================
"""


import pandas as pd 
import numpy as np 
import os

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
    
    # Browse through all the data 
    for fich in os.listdir('../../data_treat/data_interpolate'):
        
        # Get the data in a dataframe to help with the process
        data = pd.read_csv(f'../../data_treat/data_interpolate/{fich}')
        
        # Automatically remove the first and last 20% of the data
        data = data.iloc[int(0.20 * len(data)):int(0.80 * len(data)), :]
        data.reset_index(drop=True, inplace=True)
        data['time'] = data['time'] - data['time'][0]
        data['nb_step'] = data['nb_step'] - data['nb_step'][0]
        
        # Get the label of the data
        mode = str(data['mode'][0])
        
        # Initialize the list of sub-data to be saved when conditions are fulfilled for this file
        data_list = []
        
        # List of the barometer values
        baro = list(data['pressure'].astype(float).values)
        
        # Condition for the elevator and escalator labels
        if mode == 'elevator' or mode == 'escalator':
            
            # Get the list of indices where a step is made in the data 
            indice_cht_step = indices_changement(list(data['nb_step'].astype(int).values))
            
            # If there are more than 5 steps made, do not save the data
            if len(indice_cht_step) > 5:
                save = False
            
            # If zero steps are made and the barometer changes substantially indicating a floor change, save the data
            elif len(indice_cht_step) == 0:
                if abs(baro[-1] - baro[0]) > 0.01:
                    data_list.append(data)
                    save = True
                    
            # Otherwise, split the data for each step and check if the conditions below are met for data lasting at least 2 seconds
            else:
                for i in range(0, len(indice_cht_step) - 1):
                    timee = list(data['time'].astype(float).values)
                    diff_time_indice = timee[indice_cht_step[i + 1]] - timee[indice_cht_step[i]]
                    
                    if diff_time_indice > 2:
                        data_bis = data.iloc[indice_cht_step[i]:indice_cht_step[i + 1], :]                        
                        data_bis.reset_index(drop=True, inplace=True)
                        data_bis['time'] = data_bis['time'] - data_bis['time'][0]
                        data_bis['nb_step'] = data_bis['nb_step'] - data_bis['nb_step'][0]
                        
                        baro_bis = list(data_bis['pressure'].astype(float).values)
                        if abs(baro_bis[-1] - baro_bis[0]) > 0.01:
                            data_list.append(data_bis)
                            save = True
                          
        # Condition for the still label: there has to be no step and no floor change according to the barometer
        if mode == 'still':
            indice_cht_step = indices_changement(list(data['nb_step'].astype(int).values))
            # print(data[data['nb_step'] > 0].reset_index(drop=True))
            # data_step = data[data['nb_step'] > 0].reset_index(drop=True)
            if len(indice_cht_step) > 0:
                # print(indice_cht_step)
                # print('false')
                save = False
            else:
                data_list.append(data)
                save = True
        
        # Condition for the stair or walk labels
        if mode == 'stair' or mode == 'walk':
            steps = list(data['nb_step'].astype(int).values)
            # If there have been only 5 steps made, do not save the data
            if steps[-1] < 5:
                # print('false')
                save = False
                
            else:
                
                steps = list(data['nb_step'].astype(int).values)
                index_0 = 0
                
                nb_data_cout = 0
                
                # Browse how many data points there are between each step
                u, c = np.unique(steps, return_counts=True)
                for idx, count in enumerate(c):
                    
                    # If there are more than 100 data points between 2 steps, there has been a break that has not been considered
                    
                    if count > 100:
                        nb_data_cout = nb_data_cout + 1
                        where = np.where(steps == u[idx])[0]
                        
                        # Get the first and last index for this number of steps
                        first_c = where[0]
                        last_c = where[-1]
                        
                        data_bis = data.iloc[index_0:first_c, :]
                        data_bis.reset_index(drop=True, inplace=True)
                        
                        index_0 = last_c
                        
                        # Split the data before and after a pause but not the break
                        if len(data_bis) > 0:
                            
                            data_bis['time'] = data_bis['time'] - data_bis['time'][0]
                            data_bis['nb_step'] = data_bis['nb_step'] - data_bis['nb_step'][0]
                            
                            # More than 5 steps have to be made
                            if data_bis['nb_step'][len(data_bis) - 1] - data_bis['nb_step'][0] > 5:
                                if mode=='stair':
                                    baro_bis = list(data_bis['pressure'].astype(float).values)
                                    if abs(baro_bis[-1] - baro_bis[0]) > 0.01:
                                        data_list.append(data_bis)
                                        save = True
                                else:
                                    data_list.append(data_bis)
                                    save = True
                            
                        # For the last step considered
                        if last_c == len(data):
                            data_bis = data.iloc[index_0:, :]
                            data_bis.reset_index(drop=True, inplace=True)
                            if len(data_bis) > 0:
                                
                                data_bis['time'] = data_bis['time'] - data_bis['time'][0]
                                data_bis['nb_step'] = data_bis['nb_step'] - data_bis['nb_step'][0]
                                
                                if data_bis['nb_step'][len(data_bis) - 1] - data_bis['nb_step'][0] > 5:
                                    if mode=='stair':
                                        baro_bis = list(data_bis['pressure'].astype(float).values)
                                        if abs(baro_bis[-1] - baro_bis[0]) > 0.01:
                                            data_list.append(data_bis)
                                            save = True
                                    else:
                                        data_list.append(data_bis)
                                        save = True
                                    
                # If there is no split to be made
                if nb_data_cout == 0:
                    data_list.append(data)
                            
                        
                
        # Save the data if the step conditions are met     
        if save == True:
            if not os.path.exists('../../data_treat/data_interpolate_sorted'):
                os.makedirs('../../data_treat/data_interpolate_sorted')
            for i, d in enumerate(data_list):
                d.to_csv(f'../../data_treat/data_interpolate_sorted/{fich.split(".")[0]}_sort_{i}.txt', header=True, index=False)

            
def sort_data_by_baro():
    """
    @brief This function sorts the data to identify and exclude errors during data collection based on the number of steps taken during the activity.
   
    @return None
    """
    print('Begin of the sorting by baro')
    save=False
    
    if not os.path.exists('../../data_treat/data_interpolate_sorted'):
        os.makedirs('../../data_treat/data_interpolate_sorted')
    
    for fich in os.listdir('../../data_treat/data_interpolate_sorted_step'):
        data=pd.read_csv(f'../../data_treat/data_interpolate_sorted_step/{fich}')
        
        
        mode=str(data['mode'][0])
        baro=list(data['pressure'].astype(float).values)
        if mode in ['elevator','escalator','stair']:
            
            if (abs(baro[-1]-baro[0])>0.01):
                data.to_csv(f'../../data_treat/data_interpolate_sorted/{fich.split(".")[0]}.txt', header=True, index=False)
                
        elif mode in ['walk','still']:
            if (abs(baro[-1]-baro[0])<0.01):
                data.to_csv(f'../../data_treat/data_interpolate_sorted/{fich.split(".")[0]}.txt', header=True, index=False)
                