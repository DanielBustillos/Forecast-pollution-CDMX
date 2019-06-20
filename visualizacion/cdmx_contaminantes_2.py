# Bibliotecas necesarias
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd

# Dataframes que contienen las correlaciones entre PM2.5, O3, PM10 y demás contaminantes
df_o3 = pd.read_csv("/home/pradel/Desktop/Forecast_CDMX_pollution/correlacion/sub_dataset/corr_o3_72.csv")
df_pm25 = pd.read_csv("/home/pradel/Desktop/Forecast_CDMX_pollution/correlacion/sub_dataset/corr_pm25_72.csv")
df_pm10 = pd.read_csv("/home/pradel/Desktop/Forecast_CDMX_pollution/correlacion/sub_dataset/corr_pm10_72.csv")

# Diccionario de colores para cada contaminante
dic_colores = {'UVA': '#543005'
               , 'UVB': '#8c510a'
               , 'PA': '#bf812d'
               , 'CO': '#dfc27d'
               , 'NO': '#a50026'
               , 'NO2': '#d73027'
               , 'NOX': '#f46d43'
               , 'O3': '#fdae61'
               , 'PM25': '#fee090'
               , 'PMCO': '#d6604d'
               , 'SO2': '#810f7c'
               , 'RH': '#abd9e9'
               , 'TMP': '#74add1'
               , 'WSP': '#4575b4'
               , 'WDR': '#313695'
               , 'PM10': '#081d58'}


# Función que crea cada trazo, es decir una línea por contaminante
def crear_trazo(df, y, color, x='horas', width=2):
    trazo = go.Scatter(x=df[x],
                       y=df[y],
                       name=y,
                       line=dict(color=color, width=width))
    return trazo


# Listas que construyen las líneas correspondientes a cada gráfica
data_o3 = [crear_trazo(df_o3, col, dic_colores[col]) for col in df_o3.columns[1:]]
data_pm25 = [crear_trazo(df_pm25, col, dic_colores[col]) for col in df_pm25.columns[1:]]
data_pm10 = [crear_trazo(df_pm10, col, dic_colores[col]) for col in df_pm10.columns[1:]]

# Se crea la app de Dash
app = dash.Dash()

# Se obtienen los nombres de los contaminantes de las columnas (no se considera la columna "horas")
nombre_contaminante = df_o3.columns[1:].tolist()

# Las opciones para elegir contaminantes se guardan usando un diccionario
opciones_contaminante = []
for contaminante in nombre_contaminante:
    opciones_contaminante.append({'label': str(contaminante), 'value': contaminante})

# Layout que crea todos los objetos que se usan en dash
app.layout = html.Div([html.Div([html.H1('Correlaciones importantes entre contaminantes',
                                 style={'color': 'white', 'font-family': 'Helvetica', 'textAlign': 'center',
                                        'background-color': 'midnightblue	', 'line-height': '1.5',
                                        'margin': '0%'}),
                                 html.H3('Estudio de la calidad del aire en la Ciudad de México *',
                                         style={'color': 'white', 'font-family': 'Helvetica', 'textAlign': 'center',
                                                'background-color': 'midnightblue', 'line-height': '1.5',
                                                'margin': '0%'})]),
                       dcc.Dropdown(id='elegir_contaminante', options=opciones_contaminante, value='UVA'),
                       dcc.Graph(id='correlaciones_o3'),
                              #   figure={'data': data_o3,
                              #           'layout': go.Layout(title='Correlaciones de O3 con otros contaminantes',
                              #                               xaxis={'title': 'Horas'},
                              #                               yaxis={'title': 'Correlación'}
                              #                               )}),
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


@app.callback(Output('correlaciones_o3', 'figure'),
              [Input('elegir_contaminante', 'value')])
def actualizar(opciones_contaminante):
    df_o3_filtro = df_o3[[opciones_contaminante]]
    data_o3_filtro = [crear_trazo(df_o3, col, dic_colores[col]) for col in df_o3_filtro.columns]
    return {'data': data_o3_filtro,
            'layout': go.Layout(title='Correlaciones de O3 con otros contaminantes',
                                                             xaxis={'title': 'Horas'},
                                                             yaxis={'title': 'Correlación'})}


if __name__ == '__main__':
    app.run_server()
