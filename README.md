# Forecast_CDMX_pollution
Repositorio del Area de Ciencia de Datos del Conacyt. Pronosticar calidad de aire y contamintes CDMX.

Se desarrollaron modelos para pronosticar los niveles de contaminación de la Ciudad de México, los contaminante pronosticados son los siguientes:

 - PM10
 - PM2.5 (en desarrollo)
 - Ozono

Los datos de contaminación y metereología son obtenidos del [portal de la calidad de aire de la CDMX ]

(http://www.aire.cdmx.gob.mx/default.php)

### Pronóstico

Para cada contaminante se desarrollaron modelos para pronosticar sus niveles con hasta 24 horas de antelación, se obtuvo un error comparable a la bibliografía. 

La siguiente gráfica muestra los valores reales y los pronosticados con 12 horas de antelación para el PM10:

![alt text](https://github.com/DanielBustillos/forecast-pollution-CDMX/blob/master/images/PM10.png?raw=true)

Para el Ozono:

![alt text](https://github.com/DanielBustillos/forecast-pollution-CDMX/blob/master/images/O3.png?raw=true)

### Ruta Crítica 

 - Añadir un modelo del pronóstico para PM2.5, este parece ser un mejor indicador de la contaminación urbana que las que se venían utilizando hasta ahora, las PM10.

 - Disminuir el error y mejorar los modelos mostrados.

 - Enriquecer la plataforma web con el modelo de PM10 y PM2.5 así como añadir más visualizaciones interactivas.

 - Mejorar el modelo usando otras variables no consideradas, por ejemplo, los incendios forestales o la emisión de ceniza volcánica.
