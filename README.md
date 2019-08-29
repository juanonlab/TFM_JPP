# TFM UNIR Análisis por rango horario

Análisis por rango horario del consumo energético de 20 hogares. 

# Artículo original

https://www.nature.com/articles/sdata2016122

# Mediciones con los datos limpiados

https://pureportal.strath.ac.uk/en/datasets/refit-electrical-load-measurements-cleaned

# Dataset con los datos limpiados

Se encuentran disponibles en:

https://pureportal.strath.ac.uk/files/62090184/CLEAN_REFIT_081116.7z


# Cómo ejecutar el proyecto

El proyecto se compone de varias de hojas de trabajo que se han creado con el software [Jupyter](https://jupyter.org/) .
Este software se ha creado con la suite [Anaconda](https://www.anaconda.com) que ya incluye Jupyter.

El primer paso es clonar el repositorio:

```
git clone https://github.com/juanonlab/TFM_JPP.git
```

Una vez clonado el proyecto es necesario editar la hoja trabajo **01_Generar_datos_limpiados_semanal_rango_horario.ipynb**. Tiene como entrada los ficheros csv originales de cada hogar. El link para la descarga de estos datos se encuentra en la sección **Dataset con los datos limpiados**.

Es necesario descomprimir en un directorio estos ficheros y modificar en la sección constantes de la hoja de trabajo la variable **DIRECTORIO_BASE**. Actualmente la ruta es **D:/anaconda/data/** pero debe modificarse a la ruta donde se ha descomprimido los ficheros.

Una vez realizado este cambio es posible lanzar la hoja de trabajo **01_Generar_datos_limpiados_semanal_rango_horario.ipynb**. Una vez terminada esta hoja se pueden ir lanzando las siguientes hojas: 02_..., 03_... para ir obteniendo las gráficas y ficheros de salida.

