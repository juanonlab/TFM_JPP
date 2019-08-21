#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Juan Pardo Palazón

# Importacion de librerias
import numpy as np
import pandas as pd
import datetime


# In[2]:


# Constantes
DIRECTORIO_BASE = 'D:/anaconda/data/'
FECHA_MINIMA = '2014-02-01'
FECHA_MAXIMA = '2015-07-01'
NOMBRE_FICHERO_ORIGEN = 'CLEAN_House' 
TAMANO_VENTANA = 30 # Ventana de rolling
CAMPO = 'Aggregate'
DECIMALES = 2


# In[3]:


def obtenerDatosFiltrados(fichero, columna):
    """Filtrar por fechas dadas y filtrar los datos de la columna pasada
    por parametro. Se devuelve los datos filtrado de la columna
     
    Argumentos:
    file -- fichero de entrada 
    column -- columna a seleccionar
    """
    # Leer fichero origen, seleccionar columna consumo total ()
    datos_hogar = pd.read_csv(DIRECTORIO_BASE + fichero +'.csv', delimiter = ',', parse_dates=[0], index_col=0)
    datos_hogar = datos_hogar[[columna]]
    
    # Filtrardo de fechas. Rango de fechas con menor rango datos faltantes
    df_filtrado_fechas = datos_hogar[(datos_hogar.index > FECHA_MINIMA) & (datos_hogar.index < FECHA_MAXIMA)]
    return df_filtrado_fechas


# In[ ]:


def limpiarDatos(dt_filtrado, rango):
    """Limpia los valores NA. para un rango dado
     
    Argumentos:
    dt_filtrado -- tabla con todos los datos 
    rango -- rango a filtrar
    """
    # Se seleccionan aquellos valores del rango hora
    # pasado por parámetro (0, 6, 12 ó 18)
    dt_filtrado_Rango = dt_filtrado[dt_filtrado_6H.Hora == rango]
    
    # Limpieza de NA
    dt_filtrado_Rango = dt_filtrado_Rango.interpolate(method ='linear', limit_direction ='forward')
    
    return dt_filtrado_Rango


# In[ ]:


def dfTransform6HFile(fichero, columna):
    """Agrupa los datos obtenidos del fichero file
    por rangos de 6H
     
    Argumentos:
    file -- fichero de entrada 
    column -- columna a seleccionar
    """
    # Obtener data frame filtrado por fechas y con la columna pasada por parametro    
    df_filtrado = obtenerDatosFiltrados(fichero, columna)
    
    # Se agrupa por rangos de 6 horas en un día
    dt_filtrado_muestreo6H = df_filtrado.resample('6H').mean()
    
    # Se inserta la columna hora
    hora = dt_filtrado_muestreo6H.index.hour
    dt_filtrado_muestreo6H = pd.concat([dt_filtrado_muestreo6H, pd.DataFrame(hora, index=dt_filtrado_muestreo6H.index)],  axis = 1)

    # Se renombran columnas
    dt_filtrado_muestreo6H.columns = [columna,'Hora'] 
    
    return dt_filtrado_muestreo6H


# In[ ]:


def generarFicheroSemanal(dt_filtrado_6H, campo):
    """Genera para esa semana los valores de consumo
    por los 4 rangos horarios (0, 6, 12, 18)
     
    Argumentos:
    dt_filtrado_6H -- datos a transformar 
    campo -- campo a seleccionar
    """
    # Limpiar datos
    datos_filtrar_0 = limpiarDatos(dt_filtrado_6H, 0)
    datos_filtrar_6 = limpiarDatos(dt_filtrado_6H, 6)
    datos_filtrar_12 = limpiarDatos(dt_filtrado_6H, 12)
    datos_filtrar_18 = limpiarDatos(dt_filtrado_6H, 18)

    # Filtrar por hora y obtener los datos agrupados por semana
    dt_filtrado_6H_Semana = datos_filtrar_0.rolling(window=TAMANO_VENTANA, center=True).mean().resample("W").mean().apply(lambda x: round(x, DECIMALES))
    w6 = datos_filtrar_6.rolling(window=TAMANO_VENTANA, center=True).mean().resample("W").mean().apply(lambda x: round(x, DECIMALES))
    w12 = datos_filtrar_12.rolling(window=TAMANO_VENTANA, center=True).mean().resample("W").mean().apply(lambda x: round(x, DECIMALES))
    w18 = datos_filtrar_18.rolling(window=TAMANO_VENTANA, center=True).mean().resample("W").mean().apply(lambda x: round(x, DECIMALES))
    
    # Preparar fichero por rangos
    dt_filtrado_6H_Semana['Rango 06-12'] = w6[campo]
    dt_filtrado_6H_Semana['Rango 12-18'] = w12[campo]
    dt_filtrado_6H_Semana['Rango 18-00'] = w18[campo]
    dt_filtrado_6H_Semana = dt_filtrado_6H_Semana.drop(columns=['Hora'])
    dt_filtrado_6H_Semana = dt_filtrado_6H_Semana.rename(columns={campo: 'Rango 00-06'})

    return dt_filtrado_6H_Semana


# In[ ]:


# Generar los ficheros con los datos filtrados
for num_hogar in range(1, 22):
    if num_hogar != 14:
    
        fichero = NOMBRE_FICHERO_ORIGEN + str(num_hogar)
        
        # Filtrar por fechas los datos del campo seleccionado
        dt_filtrado_6H = dfTransform6HFile(fichero, CAMPO)
        
        # Generar fichero con los valores energéticos agrupados por fechas
        dt_filtrado_6H_Semana  = generarFicheroSemanal(dt_filtrado_6H, CAMPO)
        
        # El hogar 6 no dispone datos del primer mes por eso se 
        # recoge desde la posición 7
        if num_hogar != 6:
            dt_filtrado_6H_Semana.iloc[2:-2, :].to_csv('Hogar_' + str(num_hogar) + '_filtro_semanal_rango.csv', sep=',', encoding='utf-8')
        else:
            dt_filtrado_6H_Semana.iloc[7:-2, :].to_csv('Hogar_' + str(num_hogar) + '_filtro_semanal_rango.csv', sep=',', encoding='utf-8')
            

