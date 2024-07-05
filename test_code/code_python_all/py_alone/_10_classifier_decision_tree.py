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


def decision_tree_gini(data,criter,split,maxi_features,maxi_depth):
    
    X_train, X_val, y_train, y_val, X_test, y_test=data
    
    clf_gini = DecisionTreeClassifier(criterion=criter,splitter=split,max_depth=maxi_depth,max_features=maxi_features)
    
    clf_gini.fit(X_train, y_train)
    
    y_pred_gini = clf_gini.predict(X_test)
    
    
    model=clf_gini
    
    return accuracy_score(y_test, y_pred_gini)*100,clf_gini,X_train.shape[0]


def write_best_model(model,best_acc,t):
    if not os.path.exists('../../data_treat/result_classifier/model'):
        os.makedirs('../../data_treat/result_classifier/model')
    onnxfile = f'../../data_treat/result_classifier/model/decisiontree_{"{0:.2f}".format(best_acc)}.onnx'
    print('Accuracy best Decision Tree: ',best_acc)
    initial_type = [('float_input', FloatTensorType([None,t]))]
    onnx_model = convert_sklearn(model, initial_types=initial_type, target_opset=12)
    with open(onnxfile, "wb") as f2:
        f2.write( onnx_model.SerializeToString())
    f2.close()
    
    
    
def inputs():
    data=pd.read_csv('../../../../data_treat/df_output_cpp_concatenate.csv')
    
    features=list(data.columns[1:])
    
    X = data.drop(columns=['mode'])
    
    X = X.values

    y , dict_label_numero=  pd.factorize(data['mode'])

    data['mode_numero']=y

    X_train_temp, X_test, y_train_temp, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    X_train, X_val, y_train, y_val = train_test_split(
        X_train_temp, y_train_temp, test_size=0.2, random_state=43
    )
    
    print(dict_label_numero)
    
    return X_train, X_val, y_train, y_val, X_test, y_test, X, y, features, dict_label_numero




def decision_tree():
    
    if not os.path.exists('../../data_treat/result_classifier'):
        os.makedirs('../../data_treat/result_classifier')
 
    critere=['gini','entropy','log_loss']
    splitter=['best','random']
    max_depth=[None,5]
    max_features=[None,'sqrt','log2']
    
    best_acc=0
    
    with open("../../data_treat/result_classifier/decision_tree_comparaison.txt", "w") as f:
        df=None
        f.write(rf'  {os.linesep}  {os.linesep}')
        f.write(rf'{os.linesep}')
        input=inputs()[0:6]
        
        
        best_para=[0,None]
        
        
        for criterion in critere:
            for split in splitter:
                for maxi_cara in max_features:
                    for depth in max_depth:
                        acc,model,t=decision_tree_gini(input,criterion,split,maxi_cara,depth)
                        
                        
                        if best_acc<acc:
                            best_criterion=criterion
                            best_split=split
                            best_maxi_cara=maxi_cara
                            best_dept=depth
                            best_acc=acc
                            best_para=[acc,best_criterion,best_split,best_maxi_cara,best_dept]
                            best_model=model
                            
    f.close()
                        
                            
    write_best_model(best_model,best_acc,t)


