[![Build Status](https://travis-ci.com/DanielBustillos/Pronostico-contaminacion-CDMX.svg?branch=master)](https://travis-ci.com/DanielBustillos/Pronostico-contaminacion-CDMX)
[![License](https://img.shields.io/pypi/l/pandas.svg)](https://github.com/pandas-dev/pandas/blob/master/LICENSE)
# Air Quality Forecast in the Metropolitan Area of   Mexico City

This repository contains a set of machine learning models to forecast the pollutants in in the Metropolitan Area of   Mexico City. The models are optimized to obtain a low false positive rate according to the levels of the [environmental contingency program](http://www.aire.cdmx.gob.mx/default.php).



Models were developed to forecast pollution levels in Mexico City, the pollutants predicted are the following:

  - PM10
  - PM2.5 (in development)
  - Ozone

  There is a [dashboard of the project](https://github.com/paupradel/calidad_aire_cdmx), developed in the Repositories, Research and Prospective Coordination (CRIP) of the National Council of Science and Technology (CONACyT).

  The aim of the dashboard is to inform the population of the Valley of Mexico in a friendly and direct way about the state of air quality in it. It consists of a dashboard that shows the current status of the air quality index, and is updated hourly. The index is obtained from the data shared by the Ministry of Environment (SEDEMA) of the Government of Mexico City and can be found here. Also using machine learning algorithms, a model that estimates the air quality index 24 hours ahead was built. The table shows this estimate as well as a line graph of the hour-to-hour estimate of the index of suspended particles less than 10 micrometers (PM10) and ozone (O3).


Pollution and meteorological data are obtained from the [CDMX air quality portal.](http://www.aire.cdmx.gob.mx/default.php)


#### -- Project Status: [On-Hold]

## Summary

For each pollutant models were developed to forecast their levels up to 24 hours in advance, an error comparable to the literature was obtained.

The following graph shows the actual and predicted values ​​12 hours in advance for the Ozone:

![alt text](https://github.com/DanielBustillos/Pronostico-contaminacion-CDMX/blob/master/assets/o3_comparacion_02-07-2019%2012:38_.png?raw=true)

- PM10 (24 hours Moving average):

![alt text](https://github.com/DanielBustillos/Pronostico-contaminacion-CDMX/blob/master/assets/o3_comparacion.png?raw=true)

The mean RMSE is about 11.59%, the next graph shows the RSME by hour:

![alt text](https://github.com/DanielBustillos/Pronostico-contaminacion-CDMX/blob/master/assets/scores.png?raw=true)

 For more info about the performance of the models, don't hesitate to contact me.


### Contributors

* [Paulina Pradel](https://github.com/paupradel) visualization and web dashboard.
* [Daniel Bustillos](https://github.com/DanielBustillos) data analysis and modelling.


### Methods Used
* Inferential Statistics
* Machine Learning
* Data Visualization
* Predictive Modeling

### Technologies
* Python
* Scikit
* Plotly
* PostGres
* Jupyter
* HTML

## Getting Started

If you want to access the forecast it is suggested to visit the dashboard directly (soon). If you need to compute the forecast, it is enough to follow the following steps:

1. Clone this repo (for help see this [tutorial](https://help.github.com/articles/cloning-a-repository/)).
2. Raw Data is being kept [here](https://github.com/DanielBustillos/Pronostico-contaminacion-CDMX/tree/master/datasets/por_hora) within this repo.


3. The forecast and data processing/transformation scripts are implemented in a data pipeline, to run it, simply run in a terminal:
  ```
  python pipeline_general/pipeline/4_predicción.ipynb
  ```

## Featured Notebooks/Analysis/Deliverables
* [Narrativa de Calidad de Aire](https://github.com/paupradel/airecdmx_narrativa)
* [DashBoard de Calidad de Aire](https://github.com/paupradel/calidad_aire_cdmx)

![tablero de calidad del aire](assets/tablero_scr.png)


## Contributing DSWG Members

Team Leads (Contacts) : [Juan Daniel Bustillos Camargo](https://github.com/DanielBustillos)(juandaniel.bucam@gmail.com)

#### Other Members:


|Name     |  Role   |
|---------|-----------------|
|Norberto Morales| Data Engineer |

## Contact
* If you haven't joined the SF Brigade Slack, [you can do that here](http://c4sf.me/slack).  
* Feel free to contact team leads with any questions or if you are interested in contributing!
