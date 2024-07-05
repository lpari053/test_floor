
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




def inputs_lift_escalator():
    
    best_feature=['mode','gyr_y_skew', 'gyr_x_skew', 'mag_x_kurt', 'gyr_z_mean', 'gyr_x_kurt', 'gyr_z_skew', 'gyr_x_aad', 'gyr_y_aad', 'mag_arc', 'gyr_z_aad', 'gyr_x_mean', 'mag_x_skew', 'gyr_arc', 'mag_y_skew', 'mag_z_skew', 'gyr_y_kurt', 'gyr_y_mean', 'gyr_x_std', 'gyr_z_std', 'baro_std', 'gyr_z_kurt', 'baro_aad', 'baro_skew', 'baro_mean', 'aad_acc_norm', 'skewness_gyro_norm', 'mag_z_kurt', 'mag_x_std', 'mag_y_std', 'acc_z_aad', 'baro_pente', 'acc_x_skew', 'acc_x_aad', 'mag_y_mean', 'kurt_mag_norm', 'std_acc_norm', 'mag_x_mean', 'acc_z_skew', 'skew_mag_norm ', 'acc_y_std', 'mag_z_std', 'skew_acc_norm', 'acc_z_kurt', 'acc_x_kurt', 'acc_x_std', 'kurt_acc_norm', 'acc_y_aad', 'mag_z_mean', 'acc_arc', 'acc_y_kurt', 'nb_step', 'acc_x_mean', 'acc_y_skew', 'mean_mag_norm', 'aad_mag_norm', 'std_gyro_norm', 'mean_gyro_norm', 'std_mag_norm', 'acc_z_mean', 'acc_y_mean', 'aad_gyro_norm']
    data = pd.read_csv('../data_treat/df_output_cpp_concatenate.csv')

    data = data.sort_values(by='mode')
    
    def map_mode_le(mode):
        if mode =='elevator':
            return 0
        elif mode=='escalator':
            return 1
        else:
            return None
    
    data['mode_numero'] = data['mode'].apply(lambda x: map_mode_le(x))
    data = data.dropna(subset=['mode_numero'])
    y=data['mode_numero'].values
    X = data.drop(columns=['mode','mode_numero']).values

    
    X_train_temp, X_test, y_train_temp, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    X_train, X_val, y_train, y_val = train_test_split(
        X_train_temp, y_train_temp, test_size=0.2, random_state=42
    )
    
    
    return X_train, X_val, y_train, y_val, X_test, y_test, X, y







def inputs_floor_changing():
    
    best_feature=['mode','gyr_y_skew', 'gyr_x_skew', 'mag_x_kurt', 'gyr_z_mean', 'gyr_x_kurt', 'gyr_z_skew', 'gyr_x_aad', 'gyr_y_aad', 'mag_arc', 'gyr_z_aad', 'gyr_x_mean', 'mag_x_skew', 'gyr_arc', 'mag_y_skew', 'mag_z_skew', 'gyr_y_kurt', 'gyr_y_mean', 'gyr_x_std', 'gyr_z_std', 'baro_std', 'gyr_z_kurt', 'baro_aad', 'baro_skew', 'baro_mean', 'aad_acc_norm', 'skewness_gyro_norm', 'mag_z_kurt', 'mag_x_std', 'mag_y_std', 'acc_z_aad', 'baro_pente', 'acc_x_skew', 'acc_x_aad', 'mag_y_mean', 'kurt_mag_norm', 'std_acc_norm', 'mag_x_mean', 'acc_z_skew', 'skew_mag_norm ', 'acc_y_std', 'mag_z_std', 'skew_acc_norm', 'acc_z_kurt', 'acc_x_kurt', 'acc_x_std', 'kurt_acc_norm', 'acc_y_aad', 'mag_z_mean', 'acc_arc', 'acc_y_kurt', 'nb_step', 'acc_x_mean', 'acc_y_skew', 'mean_mag_norm', 'aad_mag_norm', 'std_gyro_norm', 'mean_gyro_norm', 'std_mag_norm', 'acc_z_mean', 'acc_y_mean', 'aad_gyro_norm']
    data = pd.read_csv('../data_treat/df_output_cpp_concatenate.csv')

    data = data.sort_values(by='mode')
    
    def map_mode(mode):
        if mode in ['stair', 'escalator', 'elevator']:
            return 1
        else:
            return 0
    
    data['mode_numero'] = data['mode'].apply(lambda x: map_mode(x))
    data = data.dropna(subset=['mode_numero'])
    
    y=data['mode_numero'].values
    X = data.drop(columns=['mode','mode_numero']).values

    
    X_train_temp, X_test, y_train_temp, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    X_train, X_val, y_train, y_val = train_test_split(
        X_train_temp, y_train_temp, test_size=0.2, random_state=42
    )
    
    
    return X_train, X_val, y_train, y_val, X_test, y_test, X, y





def inputs_when_yes():
    
    data = pd.read_csv('../data_treat/df_output_cpp_concatenate.csv')

    data = data.sort_values(by='mode')
    
    def map_mode_yes(mode):
        if mode== 'elevator':
            return 0
        elif mode=='escalator':
            return 1
        elif mode == 'stair':
            return 2
        else:
            return None
    
    data['mode_numero'] = data['mode'].apply(lambda x: map_mode_yes(x))
    data = data.dropna(subset=['mode_numero'])

    y=data['mode_numero'].values
    X = data.drop(columns=['mode','mode_numero']).values
    
    
    X_train_temp, X_test, y_train_temp, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    X_train, X_val, y_train, y_val = train_test_split(
        X_train_temp, y_train_temp, test_size=0.2, random_state=42
    )
    
    
    return X_train, X_val, y_train, y_val, X_test, y_test, X, y







def inputs_when_no():
    
    best_feature=['mode','gyr_y_skew', 'gyr_x_skew', 'mag_x_kurt', 'gyr_z_mean', 'gyr_x_kurt', 'gyr_z_skew', 'gyr_x_aad', 'gyr_y_aad', 'mag_arc', 'gyr_z_aad', 'gyr_x_mean', 'mag_x_skew', 'gyr_arc', 'mag_y_skew', 'mag_z_skew', 'gyr_y_kurt', 'gyr_y_mean', 'gyr_x_std', 'gyr_z_std', 'baro_std', 'gyr_z_kurt', 'baro_aad', 'baro_skew', 'baro_mean', 'aad_acc_norm', 'skewness_gyro_norm', 'mag_z_kurt', 'mag_x_std', 'mag_y_std', 'acc_z_aad', 'baro_pente', 'acc_x_skew', 'acc_x_aad', 'mag_y_mean', 'kurt_mag_norm', 'std_acc_norm', 'mag_x_mean', 'acc_z_skew', 'skew_mag_norm ', 'acc_y_std', 'mag_z_std', 'skew_acc_norm', 'acc_z_kurt', 'acc_x_kurt', 'acc_x_std', 'kurt_acc_norm', 'acc_y_aad', 'mag_z_mean', 'acc_arc', 'acc_y_kurt', 'nb_step', 'acc_x_mean', 'acc_y_skew', 'mean_mag_norm', 'aad_mag_norm', 'std_gyro_norm', 'mean_gyro_norm', 'std_mag_norm', 'acc_z_mean', 'acc_y_mean', 'aad_gyro_norm']
    data = pd.read_csv('../data_treat/df_output_cpp_concatenate.csv')

    data = data.sort_values(by='mode')
    
    def map_mode_no(mode):
        if mode== 'still':
            return 0
        elif mode=='walk':
            return 1
        else:
            return None
    
    data['mode_numero'] = data['mode'].apply(lambda x: map_mode_no(x))
    data = data.dropna(subset=['mode_numero'])

    y=data['mode_numero'].values
    X = data.drop(columns=['mode','mode_numero']).values
    
    
    X_train_temp, X_test, y_train_temp, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    X_train, X_val, y_train, y_val = train_test_split(
        X_train_temp, y_train_temp, test_size=0.2, random_state=42
    )
    
    
    return X_train, X_val, y_train, y_val, X_test, y_test, X, y





def xgboost():

    X_train, X_val, y_train, y_val, X_test, y_test, X, y=inputs_floor_changing()

    max_depths = [3, 5, 7]
    learning_rates = [0.05, 0.1, 0.15, 0.01]
    n_estimators_list = [50, 100, 150, 200, 300]
    gammas = [0, 0.5, 1]
    min_child_weights = [1, 5, 10]
    
    best_accuracy = 0.0
    best_model = None
    best_params = None
    
    for depth in max_depths:
        for lr in learning_rates:
            for n_esti in n_estimators_list:
                clf_xgb = XGBClassifier(max_depth=depth, learning_rate=lr, n_estimators=n_esti,
                                        min_child_weight=1, gamma=1).fit(X_train, y_train)
            
                y_pred = clf_xgb.predict(X_test)
                accuracy = accuracy_score(y_test, y_pred)
            
                print(f"Accuracy: {accuracy:.2f}")
                
                if accuracy > best_accuracy:
                    best_accuracy = accuracy
                    best_model = clf_xgb
                    best_params = {'max_depth': depth, 'learning_rate': lr, 'n_estimators': n_esti}
    
    print("Best parameters:", best_params)
    print("Best accuracy:", best_accuracy)
    
    onnx_model_path = f"../data_treat/result_classifier/model/xgboost_floor_changing{'{0:.2f}'.format(accuracy)}.onnx"
    
    initial_type = [('float_input', FloatTensorType([None,X_train.shape[1]]))]
    
    onnx_model = onnxmltools.convert.convert_xgboost(best_model, initial_types=initial_type, target_opset=8)
    onnx.save(onnx_model, onnx_model_path)

def xgboost_when_yes():

    X_train, X_val, y_train, y_val, X_test, y_test, X, y=inputs_when_yes()

    max_depths = [3, 5, 7]
    learning_rates = [0.05, 0.1, 0.15, 0.01]
    n_estimators_list = [50, 100, 150, 200, 300]
    gammas = [0, 0.5, 1]
    min_child_weights = [1, 5, 10]
    
    best_accuracy = 0.0
    best_model = None
    best_params = None
    
    for depth in max_depths:
        for lr in learning_rates:
            for n_esti in n_estimators_list:
                clf_xgb = XGBClassifier(max_depth=depth, learning_rate=lr, n_estimators=n_esti,
                                        min_child_weight=1, gamma=1).fit(X_train, y_train)
            
                y_pred = clf_xgb.predict(X_test)
                accuracy = accuracy_score(y_test, y_pred)
            
                print(f"Accuracy: {accuracy:.2f}")
                
                if accuracy > best_accuracy:
                    best_accuracy = accuracy
                    best_model = clf_xgb
                    best_params = {'max_depth': depth, 'learning_rate': lr, 'n_estimators': n_esti}
    
    print("Best parameters:", best_params)
    print("Best accuracy:", best_accuracy)
    
    onnx_model_path = f"../data_treat/result_classifier/model/xgboost_yes{'{0:.2f}'.format(accuracy)}.onnx"
    
    initial_type = [('float_input', FloatTensorType([None,X_train.shape[1]]))]
    
    onnx_model = onnxmltools.convert.convert_xgboost(best_model, initial_types=initial_type, target_opset=8)
    onnx.save(onnx_model, onnx_model_path)

def xgboost_when_no():

    X_train, X_val, y_train, y_val, X_test, y_test, X, y=inputs_when_no()

    max_depths = [3, 5, 7]
    learning_rates = [0.05, 0.1, 0.15, 0.01]
    n_estimators_list = [50, 100, 150, 200, 300]
    gammas = [0, 0.5, 1]
    min_child_weights = [1, 5, 10]
    
    best_accuracy = 0.0
    best_model = None
    best_params = None
    
    for depth in max_depths:
        for lr in learning_rates:
            for n_esti in n_estimators_list:
                clf_xgb = XGBClassifier(max_depth=depth, learning_rate=lr, n_estimators=n_esti,
                                        min_child_weight=1, gamma=1).fit(X_train, y_train)
            
                y_pred = clf_xgb.predict(X_test)
                accuracy = accuracy_score(y_test, y_pred)
            
                print(f"Accuracy: {accuracy:.2f}")
                
                if accuracy > best_accuracy:
                    best_accuracy = accuracy
                    best_model = clf_xgb
                    best_params = {'max_depth': depth, 'learning_rate': lr, 'n_estimators': n_esti}
    
    print("Best parameters:", best_params)
    print("Best accuracy:", best_accuracy)
    
    onnx_model_path = f"../data_treat/result_classifier/model/xgboost_no{'{0:.2f}'.format(accuracy)}.onnx"
    
    initial_type = [('float_input', FloatTensorType([None,X_train.shape[1]]))]
    
    onnx_model = onnxmltools.convert.convert_xgboost(best_model, initial_types=initial_type, target_opset=8)
    onnx.save(onnx_model, onnx_model_path)
    
    
def xgboost_when_lift_escalator():

    X_train, X_val, y_train, y_val, X_test, y_test, X, y=inputs_lift_escalator()

    max_depths = [3, 5, 7]
    learning_rates = [0.05, 0.1, 0.15, 0.01]
    n_estimators_list = [50, 100, 150, 200, 300]
    gammas = [0, 0.5, 1]
    min_child_weights = [1, 5, 10]
    
    best_accuracy = 0.0
    best_model = None
    best_params = None
    
    for depth in max_depths:
        for lr in learning_rates:
            for n_esti in n_estimators_list:
                clf_xgb = XGBClassifier(max_depth=depth, learning_rate=lr, n_estimators=n_esti,
                                        min_child_weight=1, gamma=1).fit(X_train, y_train)
            
                y_pred = clf_xgb.predict(X_test)
                accuracy = accuracy_score(y_test, y_pred)
            
                print(f"Accuracy: {accuracy:.2f}")
                
                if accuracy > best_accuracy:
                    best_accuracy = accuracy
                    best_model = clf_xgb
                    best_params = {'max_depth': depth, 'learning_rate': lr, 'n_estimators': n_esti}
    
    print("Best parameters:", best_params)
    print("Best accuracy:", best_accuracy)
    
    onnx_model_path = f"../data_treat/result_classifier/model/xgboost_le{'{0:.2f}'.format(accuracy)}.onnx"
    
    initial_type = [('float_input', FloatTensorType([None,X_train.shape[1]]))]
    
    onnx_model = onnxmltools.convert.convert_xgboost(best_model, initial_types=initial_type, target_opset=8)
    onnx.save(onnx_model, onnx_model_path)



# xgboost()
# xgboost_when_yes()
# xgboost_when_no()

