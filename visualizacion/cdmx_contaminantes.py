import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import re

# Dataframes que contienen las correlaciones entre PM2.5, O3, PM10 y demás contaminantes
df_o3 = pd.read_csv("/home/pradel/Desktop/Forecast_CDMX_pollution/correlacion/sub_dataset/corr_o3_72.csv")
df_pm25 = pd.read_csv("/home/pradel/Desktop/Forecast_CDMX_pollution/correlacion/sub_dataset/corr_pm25_72.csv")
df_pm10 = pd.read_csv("/home/pradel/Desktop/Forecast_CDMX_pollution/correlacion/sub_dataset/corr_pm10_72.csv")

# Gráficas para mostrar correlaciones entre el O3 y los demás contaminantes. Se construye en plotly una gráfica
# de línea por cada contaminante 
uva_o3 = go.Scatter(
    x=df_o3['horas'],
    y=df_o3['UVA'],
    name='UVA',
    line=dict(
        color='#000000',
        width=2)
)
uvb_o3 = go.Scatter(
    x=df_o3['horas'],
    y=df_o3['UVB'],
    name='UVB',
    line=dict(
        color='#004949',
        width=2)
)
pa_o3 = go.Scatter(
    x=df_o3['horas'],
    y=df_o3['PA'],
    name='PA',
    line=dict(
        color='#009292',
        width=2)
)
co_o3 = go.Scatter(
    x=df_o3['horas'],
    y=df_o3['CO'],
    name='CO',
    line=dict(
        color='#ff6db6',
        width=2)
)
no_o3 = go.Scatter(
    x=df_o3['horas'],
    y=df_o3['NO'],
    name='NO',
    line=dict(
        color='#ffb6db',
        width=2)
)
no2_o3 = go.Scatter(
    x=df_o3['horas'],
    y=df_o3['NO2'],
    name='NO2',
    line=dict(
        color='#490092',
        width=2)
)
nox_o3 = go.Scatter(
    x=df_o3['horas'],
    y=df_o3['NOX'],
    name='NOX',
    line=dict(
        color='#006ddb',
        width=2)
)
o3_o3 = go.Scatter(
    x=df_o3['horas'],
    y=df_o3['O3'],
    name='O3',
    line=dict(
        color='#b66dff',
        width=2)
)
pm25_o3 = go.Scatter(
    x=df_o3['horas'],
    y=df_o3['PM25'],
    name='PM2.5',
    line=dict(
        color='#6db6ff',
        width=2)
)
pmco_o3 = go.Scatter(
    x=df_o3['horas'],
    y=df_o3['PMCO'],
    name='PMCO',
    line=dict(
        color='#b6dbff',
        width=2)
)
so2_o3 = go.Scatter(
    x=df_o3['horas'],
    y=df_o3['SO2'],
    name='SO2',
    line=dict(
        color='#920000',
        width=2)
)
rh_o3 = go.Scatter(
    x=df_o3['horas'],
    y=df_o3['RH'],
    name='RH',
    line=dict(
        color='#924900',
        width=2)
)
tmp_o3 = go.Scatter(
    x=df_o3['horas'],
    y=df_o3['TMP'],
    name='TMP',
    line=dict(
        color='#db6d00',
        width=2)
)
wsp_o3 = go.Scatter(
    x=df_o3['horas'],
    y=df_o3['WSP'],
    name='WSP',
    line=dict(
        color='#ffff6d',
        width=2)
)
wdr_o3 = go.Scatter(
    x=df_o3['horas'],
    y=df_o3['WDR'],
    name='WDR',
    line=dict(
        color='#24ff24',
        width=2)
)
pm10_o3 = go.Scatter(
    x=df_o3['horas'],
    y=df_o3['PM10'],
    name='PM10',
    line=dict(
        color='rgb(205, 12, 24)',
        width=2)
)

# Gráficas para mostrar correlaciones entre PM2.5 y los demás contaminantes. Se construye en plotly una gráfica
# de línea por cada contaminante 
uva_pm25 = go.Scatter(
    x=df_pm25['horas'],
    y=df_pm25['UVA'],
    name='UVA',
    line=dict(
        color='#000000',
        width=2)
)
uvb_pm25 = go.Scatter(
    x=df_pm25['horas'],
    y=df_pm25['UVB'],
    name='UVB',
    line=dict(
        color='#004949',
        width=2)
)
pa_pm25 = go.Scatter(
    x=df_pm25['horas'],
    y=df_pm25['PA'],
    name='PA',
    line=dict(
        color='#009292',
        width=2)
)
co_pm25 = go.Scatter(
    x=df_pm25['horas'],
    y=df_pm25['CO'],
    name='CO',
    line=dict(
        color='#ff6db6',
        width=2)
)
no_pm25 = go.Scatter(
    x=df_pm25['horas'],
    y=df_pm25['NO'],
    name='NO',
    line=dict(
        color='#ffb6db',
        width=2)
)
no2_pm25 = go.Scatter(
    x=df_pm25['horas'],
    y=df_pm25['NO2'],
    name='NO2',
    line=dict(
        color='#490092',
        width=2)
)
nox_pm25 = go.Scatter(
    x=df_pm25['horas'],
    y=df_pm25['NOX'],
    name='NOX',
    line=dict(
        color='#006ddb',
        width=2)
)
o3_pm25 = go.Scatter(
    x=df_pm25['horas'],
    y=df_pm25['O3'],
    name='O3',
    line=dict(
        color='#b66dff',
        width=2)
)
pm25_pm25 = go.Scatter(
    x=df_pm25['horas'],
    y=df_pm25['PM25'],
    name='PM2.5',
    line=dict(
        color='#6db6ff',
        width=2)
)
pmco_pm25 = go.Scatter(
    x=df_pm25['horas'],
    y=df_pm25['PMCO'],
    name='PMCO',
    line=dict(
        color='#b6dbff',
        width=2)
)
so2_pm25 = go.Scatter(
    x=df_pm25['horas'],
    y=df_pm25['SO2'],
    name='SO2',
    line=dict(
        color='#920000',
        width=2)
)
rh_pm25 = go.Scatter(
    x=df_pm25['horas'],
    y=df_pm25['RH'],
    name='RH',
    line=dict(
        color='#924900',
        width=2)
)
tmp_pm25 = go.Scatter(
    x=df_pm25['horas'],
    y=df_pm25['TMP'],
    name='TMP',
    line=dict(
        color='#db6d00',
        width=2)
)
wsp_pm25 = go.Scatter(
    x=df_pm25['horas'],
    y=df_pm25['WSP'],
    name='WSP',
    line=dict(
        color='#ffff6d',
        width=2)
)
wdr_pm25 = go.Scatter(
    x=df_pm25['horas'],
    y=df_pm25['WDR'],
    name='WDR',
    line=dict(
        color='#24ff24',
        width=2)
)
pm10_pm25 = go.Scatter(
    x=df_pm25['horas'],
    y=df_pm25['PM10'],
    name='PM10',
    line=dict(
        color='rgb(205, 12, 24)',
        width=2)
)

# Gráficas para mostrar correlaciones entre PM2.5 y los demás contaminantes. Se construye en plotly una gráfica
# de línea por cada contaminante 
uva_pm10 = go.Scatter(
    x=df_pm10['horas'],
    y=df_pm10['UVA'],
    name='UVA',
    line=dict(
        color='#000000',
        width=2)
)
uvb_pm10 = go.Scatter(
    x=df_pm10['horas'],
    y=df_pm10['UVB'],
    name='UVB',
    line=dict(
        color='#004949',
        width=2)
)
pa_pm10 = go.Scatter(
    x=df_pm10['horas'],
    y=df_pm10['PA'],
    name='PA',
    line=dict(
        color='#009292',
        width=2)
)
co_pm10 = go.Scatter(
    x=df_pm10['horas'],
    y=df_pm10['CO'],
    name='CO',
    line=dict(
        color='#ff6db6',
        width=2)
)
no_pm10 = go.Scatter(
    x=df_pm10['horas'],
    y=df_pm10['NO'],
    name='NO',
    line=dict(
        color='#ffb6db',
        width=2)
)
no2_pm10 = go.Scatter(
    x=df_pm10['horas'],
    y=df_pm10['NO2'],
    name='NO2',
    line=dict(
        color='#490092',
        width=2)
)
nox_pm10 = go.Scatter(
    x=df_pm10['horas'],
    y=df_pm10['NOX'],
    name='NOX',
    line=dict(
        color='#006ddb',
        width=2)
)
o3_pm10 = go.Scatter(
    x=df_pm10['horas'],
    y=df_pm10['O3'],
    name='O3',
    line=dict(
        color='#b66dff',
        width=2)
)
pm25_pm10 = go.Scatter(
    x=df_pm10['horas'],
    y=df_pm10['PM25'],
    name='PM2.5',
    line=dict(
        color='#6db6ff',
        width=2)
)
pmco_pm10 = go.Scatter(
    x=df_pm10['horas'],
    y=df_pm10['PMCO'],
    name='PMCO',
    line=dict(
        color='#b6dbff',
        width=2)
)
so2_pm10 = go.Scatter(
    x=df_pm10['horas'],
    y=df_pm10['SO2'],
    name='SO2',
    line=dict(
        color='#920000',
        width=2)
)
rh_pm10 = go.Scatter(
    x=df_pm10['horas'],
    y=df_pm10['RH'],
    name='RH',
    line=dict(
        color='#924900',
        width=2)
)
tmp_pm10 = go.Scatter(
    x=df_pm10['horas'],
    y=df_pm10['TMP'],
    name='TMP',
    line=dict(
        color='#db6d00',
        width=2)
)
wsp_pm10 = go.Scatter(
    x=df_pm10['horas'],
    y=df_pm10['WSP'],
    name='WSP',
    line=dict(
        color='#ffff6d',
        width=2)
)
wdr_pm10 = go.Scatter(
    x=df_pm10['horas'],
    y=df_pm10['WDR'],
    name='WDR',
    line=dict(
        color='#24ff24',
        width=2)
)
pm10_pm10 = go.Scatter(
    x=df_pm10['horas'],
    y=df_pm10['PM10'],
    name='PM10',
    line=dict(
        color='rgb(205, 12, 24)',
        width=2)
)

data_o3 = [uva_o3, uvb_o3, pa_o3, co_o3, no_o3, no2_o3, nox_o3, o3_o3, pm25_o3, pmco_o3, so2_o3,
           rh_o3, tmp_o3, wsp_o3, wdr_o3, pm10_o3]

data_pm25 = [uva_pm25, uvb_pm25, pa_pm25, co_pm25, no_pm25, no2_pm25, nox_pm25, o3_pm25, pm25_pm25, pmco_pm25, so2_pm25,
             rh_pm25, tmp_pm25, wsp_pm25, wdr_pm25, pm10_pm25]

data_pm10 = [uva_pm10, uvb_pm10, pa_pm10, co_pm10, no_pm10, no2_pm10, nox_pm10, o3_pm10, pm25_pm10, pmco_pm10, so2_pm10,
             rh_pm10, tmp_pm10, wsp_pm10, wdr_pm10, pm10_pm10]

app = dash.Dash()

nombre_contaminante = df_o3.columns.tolist()
regex = re.compile('horas')

nombre_contaminante = [i for i in nombre_contaminante if not regex.search(i)]

opciones_contaminante = []
for contaminante in nombre_contaminante:
    opciones_contaminante.append({'label': str(contaminante), 'value': contaminante})

app.layout = html.Div([html.Div([html.H1('Correlaciones importantes entre contaminantes',
                                 style={'color': 'white', 'font-family': 'Helvetica', 'textAlign': 'center',
                                        'background-color': 'midnightblue	', 'line-height': '1.5',
                                        'margin': '0%'}),
                                 html.H3('Estudio de la calidad del aire en la Ciudad de México *',
                                         style={'color': 'white', 'font-family': 'Helvetica', 'textAlign': 'center',
                                                'background-color': 'midnightblue', 'line-height': '1.5',
                                                'margin': '0%'})]),
                       dcc.Dropdown(id='elegir_contaminante', options=opciones_contaminante, value=['PM10']),
                       dcc.Graph(id='correlaciones_o3',
                                 figure={'data': data_o3,
                                         'layout': go.Layout(title='Correlaciones de O3 con otros contaminantes',
                                                             xaxis={'title': 'Horas'},
                                                             yaxis={'title': 'Correlación'}
                                                             )}),
                       dcc.Graph(id='correlaciones_pm25',
                                 figure={'data': data_pm25,
                                         'layout': go.Layout(title='Correlaciones de PM2.5 con otros contaminantes',
                                                             xaxis={'title': 'Horas'},
                                                             yaxis={'title': 'Correlación'}
                                                             )}),
                       dcc.Graph(id='correlaciones_pm10',
                                 figure={'data': data_pm10,
                                         'layout': go.Layout(title='Correlaciones de PM10 con otros contaminantes',
                                                             xaxis={'title': 'Horas'},
                                                             yaxis={'title': 'Correlación'}
                                                             )}),
                       html.Div(html.P('* Los resultados aquí mostrados son parte de un estudio de la calidad del '
                                       'aire de la Ciudad de México. Se muestran las correlaciones desde las 0 '
                                       'hasta las 72 horas de los tres contaminantes considerados para '
                                       'determinar una contingencia (O3, PM10 y PM2.5) con otros contaminantes.',
                                       style={'color': 'white', 'font-family': 'Helvetica', 'textAlign': 'right',
                                        'background-color': 'midnightblue	', 'line-height': '2.0',
                                        'margin': '0%'}))
                       ])

@app.callback(Output('correlaciones_o3','correlaciones_pm25','correlaciones_pm10','figure',
             [Input('elegir_contaminante','value')]))

def actualizar(seleccion_contaminante):
    # Datos seleccionados del menú desplegable
    df_o3_filtro = df_o3[nombre_contaminante]
    df_pm25_filtro = df_pm25[nombre_contaminante]
    df_pm10_filtro = df_pm10[nombre_contaminante]

    traces = []

    traces.append(go.Scatter()


if __name__ == '__main__':
    app.run_server()
