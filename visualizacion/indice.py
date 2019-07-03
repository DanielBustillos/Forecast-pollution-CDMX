import pandas as pd
import datetime

df = pd.read_csv('/home/pradel/Downloads/datos_pau.csv', parse_dates=['fecha'], error_bad_lines=False)
df = df.sort_values(['fecha'], ascending=[0])
rango=len(df.index)
df['indice']=list(range(rango))
df.set_index('indice', inplace=True)

# Fecha adelantada 24 horas
def asignar_fecha(row, columna):
    nueva_fecha = row[columna] + datetime.timedelta(hours=24)
    return nueva_fecha

# Conversión de unidades de microgramo/metro_cúbico a ppb(partículas por billón)
def convertir_ppb(row, columna):
    ppb = row[columna]/1.96
    return ppb

# Cálculo del índice de calidad del aire para el PM10 (usando datos en microgramo/metro_cúbico)
def indice_PM10(row, columna):
    if row[columna]>=0 and row[columna]<=40:
        indice=1.2500*(row[columna])
        return round(indice)
    if row[columna]>=41 and row[columna]<=75:
        indice=(1.4412*(row[columna]-41))+51
        return round(indice)
    if row[columna]>=76 and row[columna]<=214:
        indice=(0.3551*(row[columna]-76))+101
        return round(indice)
    if row[columna]>=215 and row[columna]<=354:
        indice=(0.3525*(row[columna]-215))+151
        return round(indice)
    if row[columna]>=355 and row[columna]<=424:
        indice=(1.4348*(row[columna]-355))+201
        return round(indice)
    if row[columna]>=425 and row[columna]<=504:
        indice=(1.2532*(row[columna]-425)+301)
        return round(indice)
    if row[columna]>=505 and row[columna]<=604:
        indice=(1.0000*(row[columna]-505)+401)
        return round(indice)

# Cálculo del índice de calidad del aire para el O3 (usando datos en ppb)
def indice_O3(row, columna):
    if row[columna]>=0 and row[columna]<=70:
        indice=0.7143*(row[columna])
        return round(indice)
    if row[columna]>=71 and row[columna]<=95:
        indice=(2.0417*(row[columna]-71))+51
        return round(indice)
    if row[columna]>=96 and row[columna]<=154:
        indice=(2.4138*(row[columna]-96))+101
        return round(indice)
    if row[columna]>=155 and row[columna]<=204:
        indice=(1.0000*(row[columna]-155))+151
        return round(indice)
    if row[columna]>=205 and row[columna]<=404:
        indice=(0.4975*(row[columna]-205))+201
        return round(indice)
    if row[columna]>=405 and row[columna]<=504:
        indice=(1.000*(row[columna]-405)+301)
        return round(indice)
    if row[columna]>=505 and row[columna]<=604:
        indice=(1.0000*(row[columna]-505)+401)
        return round(indice)

dfi['fecha_24'] = dfi.apply(lambda row: asignar_fecha(row, 'fecha'), axis=1)
dfi['PM10_ppb'] = dfi.apply(lambda row: convertir_ppb(row, 'PM10'), axis=1)
dfi['PM10_pronostico_ppb'] = dfi.apply(lambda row: convertir_ppb(row, 'PM10_pronóstico'), axis=1)
dfi['indice_PM10'] = dfi.apply(lambda row: indice_PM10(row, 'PM10mean_y'), axis=1)
dfi['indice_O3'] = dfi.apply(lambda row: indice_O3(row, 'O3_y'), axis=1)
dfi['indice_pronostico_PM10'] = dfi.apply(lambda row: indice_PM10(row, 'PM10_pronóstico'), axis=1)
dfi['indice_pronostico_O3'] = dfi.apply(lambda row: indice_O3(row, 'O3_pronóstico'), axis=1)
dfi = dfi[['fecha', 'fecha_24', 'O3_pronóstico', 'PM10_pronóstico', 'O3', 'PM10', 'PM10_pronostico_ppb',
          'PM10_ppb', 'indice_O3', 'indice_PM10', 'indice_pronostico_O3', 'indice_pronostico_PM10']]

dfi.to_csv(r'/home/pradel/Desktop/Forecast_CDMX_pollution/visualizacion/indice_aire.csv')