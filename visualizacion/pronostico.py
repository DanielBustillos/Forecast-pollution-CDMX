# Bibliotecas necesarias
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd

# Dataframes que contienen las correlaciones entre PM2.5, O3, PM10 y demás contaminantes
df = pd.read_csv("/home/pradel/Downloads/datos_pau.csv")
df = df.sort_values(['fecha'], ascending=[0])

# Diccionario de colores para cada contaminante
dic_colores = {'O3_pronóstico': '#d73027'
               , 'PM10_pronóstico': '#9970ab'
               , 'O3_y_frcst_12': '#313695'
               , 'PM10mean_y_frcst_12': '#40004b'
               , 'TMP_x': '#80cdc1'
               , 'TMP_y': '#003c30'
               , 'O3_y': '#a50026'
               , 'O3': '#f46d43'
               , 'O3_x': '#fdae61'
               , 'RH': '#c51b7d'
               , 'TMP': '#35978f'
               , 'PM10': '#542788'
               , 'PM10_y': '#9970ab'
               , 'PM10_x': '#c2a5cf'
               , 'PM10mean_y': '#762a83'}

dic_etiquetas = {'O3_pronóstico': 'Pronóstico de O3'
                 , 'PM10_pronóstico': 'Pronóstico de PM10'
                 , 'O3_y_frcst_12': 'Pronóstico histórico de O3'
                 , 'PM10mean_y_frcst_12': 'Pronóstico histórico de PM10'
                 , 'TMP_x': 'Temperatura mínima'
                 , 'TMP_y': 'Temperatura máxima'
                 , 'O3_y': 'O3 máximo'
                 , 'O3': 'O3 promedio'
                 , 'O3_x': 'O3 mínimo'
                 , 'RH': 'Humedad relativa'
                 , 'TMP': 'Temperatura promedio'
                 , 'PM10': 'PM10 promedio'
                 , 'PM10_y': 'PM10 máximo'
                 , 'PM10_x': 'PM10 mínimo'
                 , 'PM10mean_y': 'PM10 promedio 24 hrs'}

# Función que crea cada trazo, es decir una línea por contaminante
def crear_trazo(df, y, name, color, x='fecha', width=2):
    trazo = go.Scatter(x=df[x],
                       y=df[y],
                       name=name,
                       line=dict(color=color, width=width))
    return trazo


# Listas que construyen las líneas correspondientes a cada gráfica
data = [crear_trazo(df, col, dic_etiquetas[col], dic_colores[col]) for col in df.columns[1:]]

# Se crea la app de Dash
app = dash.Dash()

opciones_contaminante = []
for valor, etiqueta in dic_etiquetas.items():
    opciones_contaminante.append({'label': str(etiqueta), 'value': valor})


# Layout que crea todos los objetos que se usan en dash
app.layout = html.Div([html.Div([html.H1('Calidad del Aire CDMX',
                                 style={'color': 'white', 'font-family': 'Helvetica', 'textAlign': 'center',
                                        'background-color': '#3690c0', 'line-height': '1.5',
                                        'margin': '0%'}),
                                 html.H3('Estudio de la calidad del aire en la Ciudad de México *',
                                         style={'color': 'white', 'font-family': 'Helvetica', 'textAlign': 'center',
                                                'background-color': '#3690c0', 'line-height': '1.5',
                                                'margin': '0%'})]),
                       html.Div([html.P('Selecciona el/los contaminantes:   ',
                                        style={'font-family': 'Helvetica', 'height': '40px', 'width': '500px',
                                       'display': 'table-cell', 'verticalAlign': 'middle', 'textAlign': 'left'}),
                                dcc.Dropdown(id='elegir_contaminante', options=opciones_contaminante,
                                    value=['O3_y', 'O3_y_frcst_12', 'O3_pronóstico'], multi=True,
                                    placeholder="Contaminantes",  style={'font-family': 'Helvetica',
                                                                        # 'height': '40px', 'width': '700px',
                                                                         'display': 'inblock-line',
                                                                         'verticalAlign': 'middle',
                                                                         'horizontalAlign': 'right'})]),
                       dcc.Graph(id='pronostico'),
                       html.Div(html.P('* Los resultados aquí mostrados son parte de un estudio de la calidad del '
                                       'aire de la Ciudad de México. Se muestran las correlaciones desde las 0 '
                                       'hasta las 72 horas de los tres contaminantes considerados para '
                                       'determinar una contingencia (O3, PM10 y PM2.5) con otros contaminantes.',
                                       style={'color': 'white', 'font-family': 'Helvetica', 'textAlign': 'right',
                                        'background-color': '#3690c0', 'line-height': '2.0',
                                        'margin': '0%'}))
                       ])


@app.callback(Output('pronostico', 'figure'),
              [Input('elegir_contaminante', 'value')])
def actualizar(opciones_contaminante):
    df_filtro = df[opciones_contaminante]
    data_filtro = [crear_trazo(df, col, dic_etiquetas[col], dic_colores[col]) for col in df_filtro.columns]

    return {'data': data_filtro,
               'layout': go.Layout(title='Pronóstico',
                                   xaxis={'title': 'Fecha'
                                          , 'tickformat': '%Y-%m-%d %H:%M'
                                          , 'tickangle': 40},
                                   yaxis={'title': 'ppm (partículas por millón)'})}


if __name__ == '__main__':
    app.run_server()
