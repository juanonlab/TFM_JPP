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
import numpy as np
import os


# In[22]:


# Constantes
NUM_WEEK = 5
DECIMALES = 2
fileBase = 'Hogar_' 
fileTailWeek = '_filtro_semanal_rango.csv'
RUTA_ACTUAL = os.path.dirname(os.path.realpath('__file__'))
DIRECTORIO_GUARDADO_IMG = 'IMG_PRED'
houseTotal = list()


# In[23]:


def getFinalRModel(series):
    X = series.values
    # train autoregression
    model = AR(X)
    model_fit = model.fit()
    window = model_fit.k_ar
    coef = model_fit.params
    return window,coef,model_fit


# In[24]:


def predictionAR(model_fit, data):
    predictions = model_fit.predict(start=len(data), end=len(data)+NUM_WEEK-1, dynamic=False)
    return predictions


# In[25]:


def getPrediction(df):
    
    house = list()
    # train,test,window,coef,model_fit
    predictionGroup = list()
    
    series = df['Rango 00-06']
    window,coef,model_fit = getFinalRModel(series)
    predictions=predictionAR(model_fit, series)
    predictionGroup.append(predictions)
    
    series = df['Rango 06-12']
    window,coef,model_fit = getFinalRModel(series)
    predictions=predictionAR(model_fit, series)
    predictionGroup.append(predictions)
    
    series = df['Rango 12-18']
    window,coef,model_fit = getFinalRModel(series)
    predictions=predictionAR(model_fit, series)
    predictionGroup.append(predictions)
    
    series = df['Rango 18-00']
    window,coef,model_fit = getFinalRModel(series)
    predictions=predictionAR(model_fit, series)
    house.append(predictions[0])  
    
    predictionGroup.append(predictions)
    
    return predictionGroup


# In[26]:


# Filtrar por fechas dadas y seleccionar columna consumo total (Aggregate)
def mostrarGrafico(to_plot, num_hogar):
    # Mostrar gráfica
    grafico_interpolado = to_plot.interpolate(method='spline', order=2)
    plot = grafico_interpolado.plot()
    pyplot.title('Previsión mensual. Hogar ' + num_hogar)
    pyplot.ylabel('Consumo de energía')
    pyplot.xticks(np.arange(5), ('Semana+1', 'Semana+2', 'Semana+3', 'Semana+4', 'Semana+5'))
    pyplot.show()
    
    # Se recoge la gráfica y se guarda en un fichero png
    fichero = os.path.join(RUTA_ACTUAL, DIRECTORIO_GUARDADO_IMG, 'Hogar_' + num_hogar + '_Prediccion.png')
    figura = plot.get_figure()
    figura.savefig(fichero)


# In[27]:


def generarFicheroPrediccion(df, num_hogar):
    #datos_predicciones = { 
    #    'Rango 00-06': df[0], 
    #    'Rango 06-12': df[1],
    #    'Rango 12-18': df[2], 
    #    'Rango 18-00': df[3]} 
    df_prediccion = pd.DataFrame(df).apply(lambda x: round(x, DECIMALES))
    df_prediccion.index.name = 'Semanas'
    df_prediccion.to_csv('Hogar_' + str(num_hogar) + '_prediccion.csv', sep=',', encoding='utf-8')


# In[28]:


def mostrarPrediccion(df, num_hogar):
    predictions = getPrediction(df)
    dfPredict = pd.DataFrame(predictions)
    # Transponer la tabla
    dfPredict = dfPredict.T
    dfPredict.columns = ['Rango 00-06','Rango 06-12','Rango 12-18','Rango 18-00']
    mostrarGrafico(dfPredict, num_hogar)
    generarFicheroPrediccion(dfPredict, num_hogar)


# In[29]:


for num_hogar in range(1, 22):
    if num_hogar != 14:
        fichero = fileBase + str(num_hogar) + fileTailWeek
        df = read_csv(fichero, delimiter = ',', parse_dates=[0], index_col=0)
        mostrarPrediccion(df, str(num_hogar))


# In[ ]:




