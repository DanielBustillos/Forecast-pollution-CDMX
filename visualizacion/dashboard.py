# Bibliotecas necesarias
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import re

# Iniciar la app de Dash
app = dash.Dash()

# Importación y estructuración del dataframe
dataframe = pd.read_csv("/home/pradel/Downloads/datos_pau.csv")
df = dataframe[['fecha', 'O3_pronóstico', 'PM10_pronóstico', 'O3_y_frcst_12', 'PM10mean_y_frcst_12', 'O3_y', 'O3'
                , 'O3_x', 'PM10', 'PM10_y', 'PM10_x', 'PM10mean_y']]
df = df.sort_values(['fecha'], ascending=[0])

# Diccionario de colores para cada contaminante
dic_colores = {'O3_pronóstico': '#a50026'
               , 'PM10_pronóstico': '#313695'
               , 'O3_y_frcst_12': '#f46d43'
               , 'PM10mean_y_frcst_12': '#74add1'
               , 'TMP_x': '#80cdc1'
               , 'TMP_y': '#003c30'
               , 'O3_y': '#d73027'
               , 'O3': '#fee090'
               , 'O3_x': '#fdae61'
               , 'RH': '#c51b7d'
               , 'TMP': '#35978f'
               , 'PM10': '#abd9e9'
               , 'PM10_y': '#023858'
               , 'PM10_x': '#e0f3f8'
               , 'PM10mean_y': '#4575b4'}

# Diccionario de etiquetas para cada contaminante
dic_etiquetas = {'O3_pronóstico': 'O3 pronóstico'
                 , 'PM10_pronóstico': 'PM10 pronóstico'
                 , 'O3_y_frcst_12': 'O3 pronóstico histórico'
                 , 'PM10mean_y_frcst_12': 'PM10 pronóstico histórico'
                 , 'O3_y': 'O3 máximo'
                 , 'O3': 'O3 mínimo'
                 , 'O3_x': 'O3 promedio'
                 , 'PM10': 'PM10 promedio'
                 , 'PM10_y': 'PM10 máximo'
                 , 'PM10_x': 'PM10 mínimo'
                 , 'PM10mean_y': 'PM10 promedio *'}


# Función que crea cada trazo, es decir una línea por contaminante y define si es sólida o punteada
def crear_trazo(df, y, name, color, x='fecha', width=2):
    regex = re.findall('pronóstico', name)
    if regex:
        trazo = go.Scatter(x=df[x],
                           y=df[y],
                           name=name,
                           line=dict(color=color, width=width, dash='dot'))
    else:
        trazo = go.Scatter(x=df[x],
                           y=df[y],
                           name=name,
                           line=dict(color=color, width=width))
    return trazo

# Guardar etiquetas en una lista
opciones_contaminante=[]
for valor, etiqueta in dic_etiquetas.items():
    opciones_contaminante.append({'label': str(etiqueta), 'value': valor})

# Layout que crea todos los objetos que se usan en dash
app.layout = html.Div([html.Div([html.H1('Calidad del Aire',
                                 style={'color': 'white', 'font-family': 'Helvetica', 'textAlign': 'center',
                                        'background-color': '#3690c0', 'line-height': '1.5',
                                        'margin': '0%','padding': 0}),
                                 html.H3('Estudio de la calidad del aire en la Ciudad de México',
                                         style={'color': 'white', 'font-family': 'Helvetica', 'textAlign': 'center',
                                                'background-color': '#3690c0', 'line-height': '1.5',
                                                'margin': '0%'})]),
                       html.Div([html.P('Selecciona el/los contaminantes:   ',
                                        style={'font-family': 'Helvetica', 'height': '40px', 'width': '500px',
                                       'display': 'table-cell', 'verticalAlign': 'middle', 'textAlign': 'left'}),
                                dcc.Dropdown(id='elegir_contaminante', options=opciones_contaminante,
                                    value=['O3_y', 'O3_y_frcst_12', 'O3_pronóstico'
                                           , 'PM10mean_y', 'PM10mean_y_frcst_12', 'PM10_pronóstico'], multi=True,
                                    placeholder="Contaminantes",  style={'font-family': 'Helvetica',
                                                                         'display': 'inblock-line',
                                                                         'verticalAlign': 'middle',
                                                                         'horizontalAlign': 'right'})]),
                       dcc.Graph(id='pronostico'),
                       html.Div(html.P('* PM10 calculado como el promedio cada 24 hrs.',
                                       style={'color': 'black', 'font-family': 'Helvetica', 'textAlign': 'right',
                                              'padding': 5, 'line-height': '1.0', 'font-size': 12}))
                       ])

# Interacciones entre el dropdown, crear los trazos y etiquetas
@app.callback(Output('pronostico', 'figure'),
              [Input('elegir_contaminante', 'value')])
def actualizar(opciones_contaminante):
    df_filtro = df[opciones_contaminante]
    data_filtro = [crear_trazo(df, col, dic_etiquetas[col], dic_colores[col]) for col in df_filtro.columns]

    return {'data': data_filtro,
            'layout': go.Layout(title='Pronóstico y valores históricos',
                                annotations=[dict(x=0.5,
                                                  y=-0.35,
                                                  showarrow=False,
                                                  text='Fecha',
                                                  xref='paper',
                                                  yref='paper')],
                                xaxis=go.layout.XAxis(
                                       automargin=True,
                                       tickangle=40,
                                       tickformatstops=[
                                           go.layout.xaxis.Tickformatstop(
                                               dtickrange=[3600000.0, None],
                                               value='%Y-%m-%d %H:%M'),
                                           go.layout.xaxis.Tickformatstop(
                                               dtickrange=[18000000.0, 1000],
                                               value='%Y-%m-%d %H')]
                                             ),
                                yaxis=go.layout.YAxis(
                                       title='ppm (partículas por millón)',
                                       dtick=25,
                                       range=[0, 155]),
                                )}


if __name__ == '__main__':
    app.run_server()
