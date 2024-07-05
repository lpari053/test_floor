"""
================================================================================
File Name: _8_concatenate_output_cpp.py
Author: PARISOT Laura
Creation Date: 26/05/2024

================================================================================
"""




import pandas as pd 
import numpy as np 
import os
import matplotlib.pyplot as plt
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
        data = pd.read_csv(f'cpp/output_cpp/{file}', delimiter=';').dropna()
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
    df.to_csv('../data_treat/df_output_cpp_concatenate_excel.csv', header=True, index=False,sep=";",decimal=".")
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
