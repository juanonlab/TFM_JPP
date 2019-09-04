#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Juan Pardo Palazón

# Importacion de librerias
from matplotlib import pyplot
import matplotlib.pyplot as plt
from pandas import read_csv
from pandas.plotting import lag_plot
import os
from sklearn.metrics import mean_squared_error
from math import sqrt
from functools import reduce
from sklearn.metrics import r2_score
import pandas as pd


# In[2]:


DECIMALES = 2


# In[3]:


def generar_df(indicador, num_hogar, index):
    datos = {'RMSE 00-06': indicador[0], 
        'RMSE 06-12': indicador[1], 
        'RMSE 12-18': indicador[2],
        'RMSE 18-00': indicador[3],
        'MEDIA RMSE': indicador[4], 
        'R2 00-06': indicador[5], 
        'R2 06-12': indicador[6],
        'R2 12-18': indicador[7],
        'R2 18-00': indicador[8]} 
    df_datos = pd.DataFrame(datos, index=[index]).apply(lambda x: round(x, DECIMALES))
    df_datos.index.name = 'Tipo Prediccion'
    return df_datos


# In[4]:


def media(lst): 
    return reduce(lambda a, b: a + b, lst) / len(lst)


# In[5]:


def generaRMSEPorRango(df_normal, df_wf, rango):
    err_norm = sqrt(mean_squared_error(df_normal['Test '+rango], df_normal['Pred '+rango])) 
    err_wf = sqrt(mean_squared_error(df_wf['Test '+rango], df_wf['Pred '+rango])) 
    return err_norm, err_wf


# In[6]:


def generaR2PorRango(df_normal, df_wf, rango):
    r2_norm = r2_score(df_normal['Test '+ rango], df_normal['Pred '+ rango])
    r2_wf = r2_score(df_wf['Test '+ rango], df_wf['Pred '+ rango])
    return r2_norm, r2_wf


# In[7]:


def calculaRMSE(df_NORMAL, df_WF):
    
    error_normG = list()
    error_wfG = list()
    
    # Calcula RMSE para todos los rangos
    err_norm, err_wf = generaRMSEPorRango(df_NORMAL,df_WF,'Rango 00-06')
    error_normG.append(err_norm)
    error_wfG.append(err_wf)
    err_norm, err_wf = generaRMSEPorRango(df_NORMAL,df_WF,'Rango 06-12')
    error_normG.append(err_norm)
    error_wfG.append(err_wf)
    err_norm, err_wf = generaRMSEPorRango(df_NORMAL,df_WF,'Rango 12-18')
    error_normG.append(err_norm)
    error_wfG.append(err_wf)
    err_norm, err_wf = generaRMSEPorRango(df_NORMAL,df_WF,'Rango 18-00')
    error_normG.append(err_norm)
    error_wfG.append(err_wf)
    error_normG.append(media(error_normG) )
    error_wfG.append(media(error_wfG))
    
    return error_normG, error_wfG


# In[8]:


def calculaR2(df_NORMAL, df_WF):
    """Lee el fichero con los datos transformados
     
    Argumentos:
    fichero -- nombre del fichero a leer
    numero_hogar -- numero de hogar a tratar
    """
    error_normG = list()
    error_wfG = list()
    
    # Test predictions
    err_norm, err_wf = generaR2PorRango(df_NORMAL,df_WF,'Rango 00-06')
    error_normG.append(err_norm)
    error_wfG.append(err_wf)
    err_norm, err_wf = generaR2PorRango(df_NORMAL,df_WF,'Rango 06-12')
    error_normG.append(err_norm)
    error_wfG.append(err_wf)
    err_norm, err_wf = generaR2PorRango(df_NORMAL,df_WF,'Rango 12-18')
    error_normG.append(err_norm)
    error_wfG.append(err_wf)
    err_norm, err_wf = generaR2PorRango(df_NORMAL,df_WF,'Rango 18-00')
    error_normG.append(err_norm)
    error_wfG.append(err_wf)
    
    return error_normG, error_wfG


# In[11]:


def leerFicheroYCalcularIndicadores(fichero, numero_hogar):
    """Lee el fichero con los datos transformados
     
    Argumentos:
    fichero -- nombre del fichero a leer
    numero_hogar -- numero de hogar a tratar
    """
    error_normG = list()
    error_wfG = list()
    df_NORMAL = read_csv(fichero + '_validacion_normalmodeloAR' + '.csv',  delimiter = ',', parse_dates=[0], index_col=0)
    df_WF = read_csv(fichero + '_validacion_wfmodeloAR' + '.csv',  delimiter = ',', parse_dates=[0], index_col=0)
    
    rmse_norm, rmse_wf = calculaRMSE(df_NORMAL, df_WF)
    r2_norm, r2_wf = calculaR2(df_NORMAL, df_WF)
    
    return rmse_norm + r2_norm, rmse_wf + r2_wf


# In[12]:


# Generar las gráficas
for num_hogar in range(1, 22):
    if num_hogar != 14:
        error_normG, error_wfG = leerFicheroYCalcularIndicadores('Hogar_' + str(num_hogar), str(num_hogar))
        #generar_fichero_rmse(error_normG, num_hogar)
        norm = generar_df(error_normG, num_hogar,'norm')
        wf = generar_df(error_wfG, num_hogar,'wf')
        df = [norm, wf]
        result = pd.concat(df)
        result.to_csv('Hogar_' + str(num_hogar) + '_RMSE_R2.csv', sep=',', encoding='utf-8')


# In[ ]:




