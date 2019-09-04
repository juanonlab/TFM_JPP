#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Juan Pardo Palazón

# Importacion de librerias
from matplotlib import pyplot
import matplotlib.pyplot as plt
from pandas import read_csv


# In[2]:


# Constantes
LIMITE = 1000
DECIMALES = 2
FICHERO = 'Medias_Y_Coeficientes_Hogares.csv'
FICHERO_SALIDA = 'Consumo_agrupado_dia_noche.csv'


# In[3]:


def mayor_consumo_tarde_noche(consumo_dia, consumo_tarde_noche):
    return 1 if (consumo_tarde_noche >= consumo_dia) else 0


# In[4]:


def leer_fichero(fichero):
    dataset = read_csv(fichero, header=0, infer_datetime_format=True, index_col=['Hogar'])
    return dataset


# In[8]:


def media(rango1, rango2):
    return (rango1 + rango2) / 2


# In[9]:


def guardar_fichero(df, fichero):
    df.to_csv(fichero, sep=',', encoding='utf-8')


# In[10]:


def calcula_medias_consumos(dataset):
    dataset['Consumo_dia'] = dataset.apply((lambda x: media(x['meanRango 06-12'], x['meanRango 12-18']) ), axis=1).apply(lambda x: round(x, DECIMALES))
    dataset['Consumo_tarde_noche'] = dataset.apply((lambda x: media(x['meanRango 00-06'], x['meanRango 18-00']) ), axis=1).apply(lambda x: round(x, DECIMALES))
    dataset['es_tarde_noche'] = dataset.apply((lambda x: mayor_consumo_tarde_noche(x['Consumo_dia'], x['Consumo_tarde_noche']) ), axis=1)
    df = dataset[['Consumo_dia','Consumo_tarde_noche','es_tarde_noche']]
    return df


# In[11]:


df = leer_fichero(FICHERO)
df_final = calcula_medias_consumos(df)
guardar_fichero(df_final, FICHERO_SALIDA)

