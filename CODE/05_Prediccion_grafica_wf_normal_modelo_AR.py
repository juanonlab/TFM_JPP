#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Juan Pardo Palazón

# Importacion de librerias
from matplotlib import pyplot
import matplotlib.pyplot as plt
from pandas import read_csv
import os


# In[2]:


# Constantes
RUTA_ACTUAL = os.path.dirname(os.path.realpath('__file__'))
DIRECTORIO_GUARDADO_IMG = 'IMG_PRED'


# In[3]:


# Configurar tamaño del gráfico y fuente inicial
pyplot.rcParams.update({'figure.figsize':(9,7), 'figure.dpi':100})
pyplot.rcParams['font.size'] = 10


# In[4]:


def mostrarGrafico(dataset, fichero, numero_hogar, rango):
    """Muestra el gráfico de la gráfica y se guarda
    la misma en un fichero png.
     
    Argumentos:
    dataset -- datos a dibujar en la gráfica
    fichero -- nombre del fichero a leer (sin el numero de hogar)
    numero_hogar -- numero de hogar a tratar
    """
    # Genera el gráfico y se establecen los ejes
    grafico_interpolado = dataset.interpolate(method='spline', order=2)
    plot = grafico_interpolado.plot(xticks = dataset.index)
    
    # Configurando la gráfica y mostrar el grafico
    plt.title('Comparativa test y predicción (' + rango +'). Hogar ' + numero_hogar, fontsize = 16)
    plt.xlabel('Semanas', fontsize = 14)
    plt.ylabel('Consumo de energía', fontsize = 14)
    plt.show()
    
    # Se recoge la gráfica y se guarda en un fichero png
    fichero = os.path.join(RUTA_ACTUAL, DIRECTORIO_GUARDADO_IMG, fichero +'_' + rango+ '_' + '.png')
    figura = plot.get_figure()
    figura.savefig(fichero)


# In[5]:


def leerFicheroYDibujarGrafica(fichero, numero_hogar):
    """Lee el fichero con los datos transformados
     
    Argumentos:
    fichero -- nombre del fichero a leer
    numero_hogar -- numero de hogar a tratar
    """
    dataset = read_csv(fichero + '.csv', header=0, index_col=['Semanas'])
    df = dataset[['Test Rango 00-06','Pred Rango 00-06']] 
    mostrarGrafico(df, fichero, numero_hogar, 'rango 00-06')
    df = dataset[['Test Rango 06-12','Pred Rango 06-12']] 
    mostrarGrafico(df, fichero, numero_hogar, 'rango 06-12')
    df = dataset[['Test Rango 12-18','Pred Rango 12-18']] 
    mostrarGrafico(df, fichero, numero_hogar, 'rango 12-18')
    df = dataset[['Test Rango 18-00','Pred Rango 18-00']] 
    mostrarGrafico(df, fichero, numero_hogar, 'rango 18-00')


# In[6]:


# Generar las gráficas
for num_hogar in range(1, 22):
    if num_hogar != 14:
        dataset = leerFicheroYDibujarGrafica('Hogar_' + str(num_hogar) + '_prediccion_normalmodeloAR', str(num_hogar))
        dataset = leerFicheroYDibujarGrafica('Hogar_' + str(num_hogar) + '_prediccion_wfmodeloAR', str(num_hogar))


# In[ ]:




