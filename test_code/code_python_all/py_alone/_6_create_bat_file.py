import pandas as pd 
import numpy as np 
import os
import seaborn
import matplotlib.pyplot as plt
import shutil
import sys

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

def create_bat():
    """
  @brief This function creates a BAT file to launch the feature extraction with the C++ files.
  
  @return None
  """
    print('Creation of the bat file')
    if os.path.exists(f'../cpp/data_to_put_in_cpp'):
        shutil.rmtree(f'../cpp/data_to_put_in_cpp')
    
    shutil.copytree(f'../../data_treat/data_cut', f'../cpp/data_to_put_in_cpp')
        

    fichier=os.listdir(f'../cpp/data_to_put_in_cpp')
    
    with open("../cpp/bat_all.bat", "w") as f:
        
        f.write("@echo off")
        f.write(f"{os.linesep}")
        f.write('g++ -o mon_executable main.cpp Sensors.cpp FeaturesCalculator.cpp Features.cpp')
        f.write(f"{os.linesep}")
        
        for fich in fichier:
            nom_output=f"{fich[0:-4]}.txt"
            f.write(f"mon_executable data_to_put_in_cpp/{fich} output_cpp/{nom_output}")
            f.write(f"{os.linesep}")

    print('Bat file created')