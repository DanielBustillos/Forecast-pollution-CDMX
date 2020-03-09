# Forecast_CDMX_pollution
Repositorio del Area de Ciencia de Datos del Conacyt. Pronosticar calidad de aire y contamintes CDMX.

Se desarrollaron modelos para pronosticar los niveles de contaminación de la Ciudad de México, los contaminante pronosticados son los siguientes:

 - PM10
 - PM2.5 (en desarrollo)
 - Ozono

Los datos de contaminación y metereología son obtenidos del [portal de la calidad de aire de la CDMX ](http://www.aire.cdmx.gob.mx/default.php)

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


# Air Quality Forecast in the Metropolitan Area of ​​Mexico City

This repository contains a set of machine learning models to forecast the pollutants in in the Metropolitan Area of ​​Mexico City. The models are optimized to obtain a low false positive rate according to the levels of the [environmental contingency program](http://www.aire.cdmx.gob.mx/default.php).



Models were developed to forecast pollution levels in Mexico City, the pollutants predicted are the following:

  - PM10
  - PM2.5 (in development)
  - Ozone


Pollution and meteorological data are obtained from the [CDMX air quality portal.](http://www.aire.cdmx.gob.mx/default.php)



#### -- Project Status: [On-Hold]

## Project Intro/Objective
For each pollutant models were developed to forecast their levels up to 24 hours in advance, an error comparable to the literature was obtained.

The following graph shows the actual and predicted values 12 hours in advance for PM10:


### Contribuitors

* [Paulina Pradel](https://github.com/paupradel) in the visualization and web dashboard section.


### Methods Used
* Inferential Statistics
* Machine Learning
* Data Visualization
* Predictive Modeling
* etc.

### Technologies
* Python
* Plotly
* PostGres
* Pandas, jupyter
* HTML


## Project Description
(Provide more detailed overview of the project.  Talk a bit about your data sources and what questions and hypothesis you are exploring. What specific data analysis/visualization and modelling work are you using to solve the problem? What blockers and challenges are you facing?  Feel free to number or bullet point things here)

## Getting Started

1. Clone this repo (for help see this [tutorial](https://help.github.com/articles/cloning-a-repository/)).
2. Raw Data is being kept [here](Repo folder containing raw data) within this repo.

    *If using offline data mention that and how they may obtain the data from the froup)*

3. Data processing/transformation scripts are being kept [here](Repo folder containing data processing scripts/notebooks)
4. etc...

*If your project is well underway and setup is fairly complicated (ie. requires installation of many packages) create another "setup.md" file and link to it here*  

5. Follow setup [instructions](Link to file)

## Featured Notebooks/Analysis/Deliverables
* [Notebook/Markdown/Slide Deck Title](link)
* [Notebook/Markdown/Slide DeckTitle](link)
* [Blog Post](link)


## Contributing DSWG Members

**Team Leads (Contacts) : [Full Name](https://github.com/[github handle])(@slackHandle)**

#### Other Members:

|Name     |  Slack Handle   |
|---------|-----------------|
|[Full Name](https://github.com/[github handle])| @johnDoe        |
|[Full Name](https://github.com/[github handle]) |     @janeDoe    |

## Contact
* If you haven't joined the SF Brigade Slack, [you can do that here](http://c4sf.me/slack).  
* Our slack channel is `#datasci-projectname`
* Feel free to contact team leads with any questions or if you are interested in contributing!
