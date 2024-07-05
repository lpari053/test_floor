import zipfile  
import os  
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import shutil
import subprocess  
import warnings 
warnings.filterwarnings('ignore')
warnings.filterwarnings("ignore", category=DeprecationWarning)

import pandas as pd 
import numpy as np 

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

from xgboost import XGBClassifier

from tensorflow.keras.layers import (Input, Conv1D, MaxPooling1D, GlobalAveragePooling1D, Dense, 
                                     Dropout, BatchNormalization, Flatten, GlobalMaxPooling1D) 
from tensorflow.keras.callbacks import ModelCheckpoint 
from tensorflow.keras.models import Model  
from keras.models import load_model 
import tensorflow as tf  
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)
import keras 

def inputs_classifier(best):
    
    best_feature=['mode','gyr_y_skew', 'gyr_x_skew', 'mag_x_kurt', 'gyr_z_mean', 'gyr_x_kurt', 'gyr_z_skew', 'gyr_x_aad', 'gyr_y_aad', 'mag_arc', 'gyr_z_aad', 'gyr_x_mean', 'mag_x_skew', 'gyr_arc', 'mag_y_skew', 'mag_z_skew', 'gyr_y_kurt', 'gyr_y_mean', 'gyr_x_std', 'gyr_z_std', 'baro_std', 'gyr_z_kurt', 'baro_aad', 'baro_skew', 'baro_mean', 'aad_acc_norm', 'skewness_gyro_norm', 'mag_z_kurt', 'mag_x_std', 'mag_y_std', 'acc_z_aad', 'baro_pente', 'acc_x_skew', 'acc_x_aad', 'mag_y_mean', 'kurt_mag_norm', 'std_acc_norm', 'mag_x_mean', 'acc_z_skew', 'skew_mag_norm ', 'acc_y_std', 'mag_z_std', 'skew_acc_norm', 'acc_z_kurt', 'acc_x_kurt', 'acc_x_std', 'kurt_acc_norm', 'acc_y_aad', 'mag_z_mean', 'acc_arc', 'acc_y_kurt', 'nb_step', 'acc_x_mean', 'acc_y_skew', 'mean_mag_norm', 'aad_mag_norm', 'std_gyro_norm', 'mean_gyro_norm', 'std_mag_norm', 'acc_z_mean', 'acc_y_mean', 'aad_gyro_norm']
    data = pd.read_csv('../../data_treat/df_output_cpp_concatenate.csv')
    data = data.sort_values(by='mode')
    if best==True:
        data=data[best_feature]
    features = list(data.columns[1:])
    
    X = data.drop(columns=['mode']).values
    y, dict_label_numero = pd.factorize(data['mode'])
    
    u,c=np.unique(y,return_counts=True)
    # print(u,c,dict_label_numero)
    min_count=min(c)
    indice=[]
    for ia in u:
        iu=np.where(y==ia)[0]
        for e in range(0,min_count-1):
            indice.append(iu[e])
    X=X[indice]
    y=y[indice]
    X_train_temp, X_test, y_train_temp, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    X_train, X_val, y_train, y_val = train_test_split(
        X_train_temp, y_train_temp, test_size=0.2, random_state=43
    )
    
    return X_train, X_val, y_train, y_val, X_test, y_test, X, y, features, dict_label_numero

"XGboost"
  
def xgboost():

    c=0
    max_depths = [3, 5, 7]
    learning_rates = [ 0.15]
    n_estimators_list = [100, 150, 200, 300]
    min_child_weights = [1, 5, 10]
    gammas = [0.5, 1, 1.5]
    
    best_accuracy = 0
    best_parameters = {}
    for best in [True,False]:
        X_train, X_val, y_train, y_val, X_test, y_test, X, y, features, dict_label_numero=inputs_classifier(best)
        for max_depth in max_depths:
            for learning_rate in learning_rates:
                for n_estimators in n_estimators_list:
                    for min_child_weight in min_child_weights:
                        for gamma in gammas:
                            clf_xgb = XGBClassifier(max_depth=max_depth, learning_rate=learning_rate, n_estimators=n_estimators,
                                                     min_child_weight=min_child_weight, gamma=gamma).fit(X_train, y_train)
                            accuracy = clf_xgb.score(X_val, y_val)
                            print(c)
                            c=c+1
                            print(accuracy)
                            if accuracy > best_accuracy:
                                print('rrrr')
                                best_accuracy = accuracy
                                best_parameters = {'best':best,'max_depth': max_depth, 'learning_rate': learning_rate,
                                                   'n_estimators': n_estimators, 'min_child_weight': min_child_weight,
                                                   'gamma': gamma}
    
    # print("Best parameters:", best_parameters)
    # print("Best accuracy:", best_accuracy)
                
    #             f_score = f1_score(y_test, y_pred, average='weighted')
    #             # print("F-score:", f_score)
                
    #             conf_matrix = confusion_matrix(y_test, y_pred)
    #             print(f"Conf Matrix {os.linesep}",conf_matrix)
                
    #             # onnx_model_path = f"../../data_treat/result_classifier/model/xgboost_{'{0:.2f}'.format(accuracy)}.onnx"
                
    #             # initial_type = [('float_input', FloatTensorType([None,X_train.shape[1]]))]
                
    #             # onnx_model = onnxmltools.convert.convert_xgboost(clf_xgb, initial_types=initial_type, target_opset=8)
    #             # onnx.save(onnx_model, onnx_model_path)
    
    print("Best parameters:", best_parameters)
    print("Best accuracy:", best_accuracy)
    