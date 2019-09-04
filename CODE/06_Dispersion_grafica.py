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


# In[2]:


# Constantes
RUTA_ACTUAL = os.path.dirname(os.path.realpath('__file__'))
TITULO = 'Gráfica dispersión. Hogar '
TITULO_NR = 'Gráfica dispersión sin rolling. Hogar '
DIRECTORIO_GUARDADO_IMG = 'IMG_DISP'


# In[3]:


# Configurar tamaño del gráfico y fuente inicial
pyplot.rcParams.update({'figure.figsize':(9,7), 'figure.dpi':100})
pyplot.rcParams['font.size'] = 10


# In[4]:


def showLagPlot(df, numero_hogar, fichero, titulo):

    # Genera el gráfico y se establecen los ejes
    seriesRange00_06 = df['Rango 00-06']
    seriesRange06_12 = df['Rango 06-12']
    seriesRange12_18 = df['Rango 12-18']
    seriesRange18_00 = df['Rango 18-00']
    
    lag_plot(seriesRange00_06, c = "blue")
    lag_plot(seriesRange06_12, c = "orange")
    lag_plot(seriesRange12_18, c = "green")
    lag_plot(seriesRange18_00, c = "red")
    
    pyplot.title(titulo + numero_hogar , fontsize = 16)
    pyplot.xlabel('y (t + 1)', fontsize = 14)
    
    pyplot.ylabel('y (t)', fontsize = 14)
    fichero = os.path.join(RUTA_ACTUAL, DIRECTORIO_GUARDADO_IMG, fichero +'_dispersion.png')
    pyplot.savefig(fichero)
    pyplot.show()


# In[5]:


def leerFicheroYDibujarGraficaDispersion(fichero, numero_hogar, titulo):
    """Lee el fichero con los datos transformados
     
    Argumentos:
    fichero -- nombre del fichero a leer
    numero_hogar -- numero de hogar a tratar
    """
    df = read_csv(fichero + '.csv',  delimiter = ',', parse_dates=[0], index_col=0)
    showLagPlot(df, numero_hogar, fichero, titulo)


# In[6]:


# Generar las gráficas
for num_hogar in range(1, 22):
    if num_hogar != 14:
        dataset = leerFicheroYDibujarGraficaDispersion('Hogar_' + str(num_hogar) + '_filtro_semanal_rango', str(num_hogar), TITULO)
        dataset = leerFicheroYDibujarGraficaDispersion('Hogar_' + str(num_hogar) + '_filtro_semanal_rango_NR', str(num_hogar), TITULO_NR)


# In[ ]:




