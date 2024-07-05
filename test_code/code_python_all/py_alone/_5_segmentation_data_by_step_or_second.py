import pandas as pd 
import numpy as np 
import os
import seaborn
import matplotlib.pyplot as plt

"""
================================================================================
Step 5: Separate Data by Step or Second
================================================================================

Function: separate_data_by_step_or_second

This function splits the input data for the feature extractor stage. It proceeds 
by considering two approaches: time and step.

For the time approach, it creates an input for every 3 seconds of the total acquisition 
time. This duration is chosen because the step counter needs approximately 1.5 seconds 
to predict a step, and for a stride (2 steps), we need 3 seconds.

For the step approach, if a stride (2 steps) is detected within the 3-second window, 
only the data between each stride (i.e., stride duration) is considered.

The function creates a folder named 'data_cut' containing the .txt files, where each 
file represents the input for the feature extractor stage implemented in a C++ code.

Input:
    fich (str): Name of the file containing the concatenated, interpolated, and sorted sensor data.

Output:
    None
"""

fich='../../data_treat/data_interpolate_sorted/valerie_28-05-2024-09-50-21-568_walk_4_sort.txt'

name=fich.split('/')[-1]

data=pd.read_csv(f'{fich}')

time=data['time']
step=data['nb_step']

index_0=0
for i in range(0,len(data)):
    
    if time[i]-time[index_0]>2 or step[i]-step[index_0]==2:
        
        data2=data.iloc[index_0:i,:]
        
        
        
        data2.to_csv(f'../../data_treat/data_cut/{name.split(".")[0]}_cut_{index_0}.txt',index=False,header=False)
    

        
        index_0=i
        







    

        