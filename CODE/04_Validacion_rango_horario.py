#!/usr/bin/env python
# coding: utf-8

# In[1]:


# https://machinelearningmastery.com/train-final-machine-learning-model/
# https://machinelearningmastery.com/autoregression-models-time-series-forecasting-python/
# https://www.statisticshowto.datasciencecentral.com/lag-plot/
# https://github.com/convergenceIM/alpha-scientist/blob/master/content/04_Walk_Forward_Modeling.ipynb
# https://www.statisticshowto.datasciencecentral.com/lag-plot/
from pandas import Series
from matplotlib import pyplot
from statsmodels.tsa.ar_model import AR
from sklearn.metrics import mean_squared_error
from pandas import read_csv
from datetime import datetime
from pandas.plotting import autocorrelation_plot
from pandas.plotting import lag_plot
from math import sqrt
import pandas as pd 
from functools import reduce
from matplotlib import pyplot
from sklearn.metrics import r2_score
import sklearn.metrics as metrics
import numpy as np


# In[2]:


# Constantes
NUMERO_TEST = 5
PREFIJO_FICHERO = 'Hogar_' 
SUFIJO_FICHERO = '_filtro_semanal_rango.csv'
DECIMALES = 2


# In[3]:


def obtenerARModelTest(series):
    X = series.values
    train, test = X[1:len(X)-NUMERO_TEST], X[len(X)-NUMERO_TEST:]
    model = AR(train)
    model_fit = model.fit()
    window = model_fit.k_ar
    coef = model_fit.params
    return train,test,window,coef,model_fit


# In[4]:


def prediccionTest_AR(model_fit, train, test):
    predictions = model_fit.predict(start=len(train), end=len(train)+len(test)-1, dynamic=False)
    return predictions


# In[5]:


def prediccionTest_AR_WF(model_fit, train, test):
    window = model_fit.k_ar
    coef = model_fit.params

    # walk forward over time steps in test
    history = train[len(train)-window:]
    history = [history[i] for i in range(len(history))]
    predictions = list()
    for t in range(len(test)):
        length = len(history)
        lag = [history[i] for i in range(length-window,length)]
        yhat = coef[0]
        for d in range(window):
            yhat += coef[d+1] * lag[window-d-1]
        obs = test[t]
        predictions.append(yhat)
        history.append(obs)  

    return predictions


# In[6]:


def calcularPrediccionesTest(df, numPred, esWF):
    # train, test, window, coef, model_fit
    predictionGroup = list()
    testGroup = list()
        
    series = df['Rango 00-06']
    train,test,window,coef,model_fit = obtenerARModelTest(series)
    predictions = prediccionTest_AR_WF(model_fit, train, test) if esWF else prediccionTest_AR(model_fit, train, test)  
    predictionGroup.append(predictions)
    testGroup.append(test)
        
    series = df['Rango 06-12']
    train,test,window,coef,model_fit = obtenerARModelTest(series)
    predictions = prediccionTest_AR_WF(model_fit, train, test) if esWF else prediccionTest_AR(model_fit, train, test)  
    predictionGroup.append(predictions)
    testGroup.append(test)
    
    series = df['Rango 12-18']
    train,test,window,coef,model_fit = obtenerARModelTest(series)
    predictions = prediccionTest_AR_WF(model_fit, train, test) if esWF else prediccionTest_AR(model_fit, train, test)  
    predictionGroup.append(predictions)
    testGroup.append(test)
    
    series = df['Rango 18-00']
    train,test,window,coef,model_fit = obtenerARModelTest(series)
    predictions = prediccionTest_AR_WF(model_fit, train, test) if esWF else prediccionTest_AR(model_fit, train, test)  
    predictionGroup.append(predictions)
    testGroup.append(test)
    
    return predictionGroup, testGroup


# In[7]:


def generar_fichero_validacion_test(df, esWF, tipo_prediccion):
    prediccion, test = calcularPrediccionesTest(df, NUMERO_TEST, esWF)
    datos_predicciones = {'Test Rango 00-06': test[0].tolist(), 
        'Pred Rango 00-06': prediccion[0], 
        'Test Rango 06-12': test[1].tolist(),
        'Pred Rango 06-12': prediccion[1],
        'Test Rango 12-18': test[2].tolist(), 
        'Pred Rango 12-18': prediccion[2], 
        'Test Rango 18-00': test[3].tolist(),
        'Pred Rango 18-00': prediccion[3]} 
    df_prediccion = pd.DataFrame(datos_predicciones).apply(lambda x: round(x, DECIMALES))
    df_prediccion.index.name = 'Semanas'
    df_prediccion.to_csv('Hogar_' + str(num_hogar) + '_validacion_' + tipo_prediccion + 'modeloAR.csv', sep=',', encoding='utf-8')


# In[8]:


def procesa_hogar(num_hogar):
    # Se compone el nombre del fichero
    fichero = PREFIJO_FICHERO + str(num_hogar) + SUFIJO_FICHERO
    # Leer el fichero
    df = read_csv(fichero, delimiter = ',', parse_dates=[0], index_col=0)
    # Prediccion Validacion Test con WalkForward
    generar_fichero_validacion_test(df, True, 'wf')
    # Prediccion Validacion Test del modelo AR normal
    generar_fichero_validacion_test(df, False, 'normal')


# In[9]:


for num_hogar in range(1, 22):
    if num_hogar != 14:
        procesa_hogar(num_hogar)

