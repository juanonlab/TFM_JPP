#!/usr/bin/env python
# coding: utf-8

# In[18]:


# Juan Pardo Palazón

# Importacion de librerias
from matplotlib import pyplot
import matplotlib.pyplot as plt
from pandas import read_csv
import pandas as pd


# In[19]:


def crearDataFrame():
    """Crea la cabecera del dataframe (df)
    """
    df = pd.DataFrame(columns=['stdRango 00-06','meanRango 00-06','coefRango 00-06'
                               ,'stdRango 06-12','meanRango 06-12','coefRango 06-12'
                               ,'stdRango 12-18','meanRango 12-18','coefRango 12-18'
                               ,'stdRango 18-00','meanRango 18-00','coefRango 18-00'])
    df.index.name = 'Hogar'
    return df


# In[20]:


def calcularDesviacionMediaCoeficiente(dataset, numeroHogar, contador, df):
    """Genera un data frame calculando la desviacion, 
    la media y el coeficiente de variabilidad para todos los rangos
     
    Argumentos:
    dataset -- datos de un hogar
    numeroHogar --- numeroHogar
    contador -- contador
    df -- dataframe
    """
    # Se calcula la desviacion y la media para cada rango
    desviacionColumnas = dataset.std(axis = 0, skipna = True) 
    mediaColumnas = dataset.mean(axis = 0, skipna = True)
    coef0 = (desviacionColumnas[0]/mediaColumnas[0])*100
    coef1 = (desviacionColumnas[1]/mediaColumnas[1])*100
    coef2 = (desviacionColumnas[2]/mediaColumnas[2])*100
    coef3 = (desviacionColumnas[3]/mediaColumnas[3])*100         

    # Se guarda en una fila los resultados y se redondea a 2 decimales
    df.loc[contador, 'stdRango 00-06'] = desviacionColumnas[0].round(2)
    df.loc[contador, 'meanRango 00-06'] = mediaColumnas[0].round(2)
    df.loc[contador, 'coefRango 00-06'] = coef0.round(2)
    df.loc[contador, 'stdRango 06-12'] = desviacionColumnas[1].round(2)
    df.loc[contador, 'meanRango 06-12'] = mediaColumnas[1].round(2)
    df.loc[contador, 'coefRango 06-12'] = coef1.round(2)
    df.loc[contador, 'stdRango 12-18'] = desviacionColumnas[2].round(2)
    df.loc[contador, 'meanRango 12-18'] = mediaColumnas[2].round(2)
    df.loc[contador, 'coefRango 12-18'] = coef2.round(2)
    df.loc[contador, 'stdRango 18-00'] = desviacionColumnas[3].round(2)
    df.loc[contador, 'meanRango 18-00'] = mediaColumnas[3].round(2)
    df.loc[contador, 'coefRango 18-00'] = coef3.round(2)

    return df


# In[21]:


def insertarFila(file_name, numero_hogar, contador, df):
    """Inserta la desviación típica, la media y el
    coeficiente de variabilidad por cada rango horario
     
    Argumentos:
    desviacionColumnas -- desviación típica de todos los rangos de un hogar
    mediaColumnas -- media de todos los rangos de un hogar
    numeroHogar -- numeroHogar
    contador -- contador
    df -- dataframe
    """
    # Se leen los datos del fichero
    dataset = read_csv(file_name + '.csv', header=0, infer_datetime_format=True, index_col=['Time'])
    
    # Calcula la desviación, la media y los coeficientes
    df = calcularDesviacionMediaCoeficiente(dataset, numero_hogar, contador, df)
    
    # Se guarda en una fila los datos obtenidos en df
    df.to_csv('Medias_Y_Coeficientes_Hogares222.csv', sep=',', encoding='utf-8')
    return df


# In[22]:


contador = 0
# Se crea un data frame vacío
# que se irá rellenando
# con las medias, coeficiente y desviación típica (std)
# para cada hogar
df = crearDataFrame()
for num_hogar in range(1, 22):
    contador += 1
    if num_hogar != 14:
        insertarFila('Hogar_' + str(num_hogar) + '_filtro_semanal_rango', str(num_hogar), contador, df)

