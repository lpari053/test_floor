"""
================================================================================
File Name: _9_feature_selector.py
Author: PARISOT Laura
Creation Date: 26/05/2024

================================================================================
"""



import pandas as pd 
import numpy as np 
import os
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split 
from sklearn.feature_selection import mutual_info_classif  
from sklearn.tree import DecisionTreeClassifier  
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix  
from sklearn.model_selection import train_test_split, StratifiedKFold

from skl2onnx import convert_sklearn 
from skl2onnx.common.data_types import FloatTensorType 
import onnx  
import onnxmltools
from onnxmltools.convert.common.data_types import FloatTensorType 
import tf2onnx 
"""
================================================================================
Step 9: Feature Selector



================================================================================

The feature extraction stage calculates a lot of features. With this function, we 
want to determine which of these features are the best ones. It uses three feature 
selector methods:

1. Information Gain (score_ig)
2. Decision Tree (scoring_tp)
3. Correlation (scoring_cls)

Each of these methods has its own function that creates its own plot to visualize 
the result and a txt file.

Input:
    None

Output:
    None
"""



def score_ig(inputs,name):
    """
    @brief Information Gain Feature Selector
    
    @return dict_ig , dictionary of information gain for each feature considered
    @rtype: dict
    """
    
    # Initialization of the dictionary that will contain the information gain for each feature considered
    dict_ig = []
    
    # Writing a txt file with the information gain value for each feature
    with open(f"../data_treat/feature_selector/information_gain_comparaison_{name}.txt", "w") as f:

        f.write(rf' {os.linesep}')
        f.write(rf' {os.linesep}')
        
        # Getting the data separated into different sub-datasets for a classification with 5 classes
        X_train, X_val, y_train, y_val, X_test, y_test, X, y, features, dict_label_numero = inputs
        
        # Launch the calculation of information gain
        ig = mutual_info_classif(X, y)
        
        ig_dict = {}
        for i in range(len(features)):
            ig_dict[features[i]] = ig[i]
            
        # Sort the dictionary to have the highest value first 
        ig_dict_sorted = dict(sorted(ig_dict.items(), key=lambda item: item[1], reverse=True))
    
        # Write the features that are above 0.5 of information gain
        selected_features_index_05 = np.where(np.array(list(ig_dict_sorted.values())) > 0.5)
        selected_features = np.array(list(ig_dict_sorted.keys()))[selected_features_index_05]
        selected_value = np.array(list(ig_dict_sorted.values()))[selected_features_index_05]
        
        f.write(rf'  above 0.5 {len(selected_features)}:   {selected_features} \n {selected_value}')
        f.write(rf' {os.linesep}')
        
        # Plot the information gain to compare each feature
        sns.set(style="whitegrid")
        sns.set(rc={'figure.figsize':(17,8)})
        sns.barplot(x=list(ig_dict_sorted.values()), y=list(ig_dict_sorted.keys()))
        
        plt.title(f'Information Gain of Features {name}')
        plt.xlabel('Information Gain')
        plt.ylabel('Feature Name')
        
        if not os.path.exists('../data_treat/graphics_feature_selector'):
            os.makedirs('../data_treat/graphics_feature_selector')
        
        plt.savefig(f'../data_treat/graphics_feature_selector/IG_{name}.png')
        plt.show()
        plt.close()
        
        f.write(rf' {os.linesep}')
        f.write(rf' {os.linesep}')
        
        dict_ig.append(ig_dict_sorted)
            
    return dict_ig


def scoring_cls(inputs,name): 
    """
    @brief Correlation Feature Selector
    
    @return dict_cls , dictionary of correlation for each feature considered
    @rtype: dict
    """
    dict_cls = []
    with open(f"../data_treat/feature_selector/cls_comparaison_{name}.txt", "w") as f:
        
        f.write(rf'    {os.linesep}')
        f.write(rf' {os.linesep}')
    
        # Getting the data separated into different sub-datasets for classification
        X_train, X_val, y_train, y_val, X_test, y_test, X, y, features, dict_label_numero = inputs

        X = pd.DataFrame(X, columns = features)
        X['mode_numero'] = y
        
        # Calculate the correlation matrix and extract correlations with the target
        corr_matrix = X.corr()
        corr_with_target = corr_matrix['mode_numero']
        k = 10
        top_k = corr_with_target.abs().sort_values()
        
        indices_sup = np.where(np.array(top_k) > 0.3)[0]
        
        f.write(f" above 0.3 {len(indices_sup)}: {top_k.index[indices_sup]} \n {top_k[indices_sup].values}")
        
        selected_features = X.iloc[:, indices_sup]
        
        # Plot the correlation values to compare each feature
        sns.set(style="whitegrid")
        sns.set(rc={'figure.figsize': (20, 12)})
        sns.barplot(x = np.array(top_k), y = list(top_k.index))
        
        plt.title(f'CLS {name}')
        plt.xlabel('CLS')
        plt.ylabel('Feature Name')
        
        if not os.path.exists('../data_treat/graphics_feature_selector'):
            os.makedirs('../data_treat/graphics_feature_selector')
        
        plt.savefig(f'../data_treat/graphics_feature_selector/CLS_{name}.png')
        plt.show()
        plt.close()
        
        f.write(rf' {os.linesep}')
        f.write(rf' {os.linesep}')
        
        dict_cls.append(top_k.to_dict())
        
    return dict_cls


def scoring_tp(inputs,name): 
    """
    @brief Tree Pruning, decision tree Feature Selector
    
    @return dict_tp , dictionary of importance in the decision tree classification for each feature used
    """
    dict_tp = []
    with open(f"../data_treat/feature_selector/tree_puning_comparaison_{name}.txt", "w") as f:
        
        f.write(rf'  {os.linesep}  {os.linesep}')
        f.write(rf' {os.linesep}')
        
        # Getting the data separated into different sub-datasets for classification
        X_train, X_val, y_train, y_val, X_test, y_test, X, y, features, dict_label_numero = inputs
    
        # Train a decision tree classifier
        clf = DecisionTreeClassifier(max_depth = 16, random_state = 8)
        clf.fit(X, y)
        
        importances = clf.feature_importances_
        
        tp_dict = {}
        for i in range(len(features)):
            tp_dict[features[i]] = importances[i]
     
        threshold = 0.020  
        
        indices = np.where(importances > threshold)
        features = np.array(features)
        selected_features = features[indices]
        importances_p = importances[indices]
        
        f.write('above 0.020 \n:')
        f.write(rf' {len(list(selected_features))} : {list(selected_features)} \n {importances_p}')
        
        # Plot the feature importances to compare each feature
        sns.set(style="whitegrid")
        sns.set(rc={'figure.figsize': (17, 8)})
        sns.barplot(x = importances, y = features)
        
        plt.title(f'Tree Pruning {name}')
        plt.xlabel('Tree Pruning')
        plt.ylabel('Feature Name')
        
        if not os.path.exists('../data_treat/graphics_feature_selector'):
            os.makedirs('../data_treat/graphics_feature_selector')
        
        plt.savefig(f'../data_treat/graphics_feature_selector/TP_{name}.png')
        plt.show()
        plt.close()
        
        f.write(rf' {os.linesep}')
        f.write(rf' {os.linesep}')
        
        dict_tp.append(tp_dict)
            
    return dict_tp


def feature_selector(inputs,name):
    """
    @brief Regroup all the information for each feature selector to find the best features for the classification
    
    @return best, list of features where their values are superior to the mean of all features
    @return list_best, list of the best 10 features based on the sum of each feature selector's values
    @return df_sort_sum, dataframe of the feature selectors with a column for the sum of each feature's value
    """
   
    if not os.path.exists('../data_treat/feature_selector'):
        os.makedirs('../data_treat/feature_selector')
        
    # Getting the dictionary for each feature selector
    dict_ig = score_ig(inputs,name)
    dict_tp = scoring_tp(inputs,name)
    dict_cls = scoring_cls(inputs,name)
    
    keys = list(dict_tp[0].keys())
    
    # Create a dataframe with each selector
    df = pd.DataFrame(index = ['Tree', 'CLS', 'IG', 'evaluation', 'sum'], columns = keys)
    
    for col in keys:
        df.loc['Tree'][col] = dict_tp[0].get(col)
        df.loc['IG'][col] = dict_ig[0].get(col)
        df.loc['CLS'][col] = dict_cls[0].get(col)
        df.loc['sum'][col] = float(dict_cls[0].get(col)) + float(dict_ig[0].get(col)) + float(dict_tp[0].get(col))
    
    # Initialize a list with the feature names that have a value for each selector above the mean
    best = []   
    for col in keys:
        if (dict_tp[0].get(col) > np.mean(df.loc['Tree'].values) and 
            dict_ig[0].get(col) > np.mean(df.loc['IG'].values) and 
            dict_cls[0].get(col) > np.mean(df.loc['CLS'].values)):
                
            df.loc['evaluation'][col] = True
            best.append(col)
        else:
            df.loc['evaluation'][col] = False
    
    df = df.T
    df = df.sort_index()
    df_sort_sum = df.sort_values(by = 'sum')
    # df.to_csv(f'../data_treat/feature_selector/feature_selector_comparaison_{name}.txt', header = True, index = True)
    df_sort_sum.to_csv(f'../data_treat/feature_selector/feature_selector_comparaison_{name}.txt', header = True, index = True)
    
    
    
    # Create a list with the best 10 features with the highest sum of selector values
    list_best = list(df_sort_sum.iloc[0:10].index)
    print(list_best)
    
    return best, list_best, df_sort_sum

