"""
================================================================================
File Name: _7_lauch_bat_file.py
Author: PARISOT Laura
Creation Date: 26/05/2024

================================================================================
"""



"""
================================================================================
Importing Libraries
================================================================================
"""
import pandas as pd 
import numpy as np 
import os
import seaborn
import matplotlib.pyplot as plt
import shutil
import sys
import subprocess


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
    if os.path.exists('../cpp/output_cpp'):
        shutil.rmtree('../cpp/output_cpp')
        
    os.makedirs('../cpp/output_cpp')
    
    # Commands to run the BAT file
    commands_to_run = [
        'cd ../cpp',
        'bat_all'
    ]
    
    # Concatenate commands
    commands_concatenated = ' && '.join(commands_to_run)
    
    # Create command to start a new command prompt and run the concatenated commands
    cmd_command = f'start cmd /k "{commands_concatenated}"'
    
    # Start the process
    import time
    process = subprocess.Popen(cmd_command, shell=True)
    
    # Wait for the process to finish
    while process.poll() is None:
        time.sleep(0.5)
        
       