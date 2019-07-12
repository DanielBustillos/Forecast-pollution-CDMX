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
dataframe = pd.read_csv("/home/pradel/Downloads/datos_pau.csv", parse_dates=['fecha'])
df = dataframe[['fecha', 'O3_max', 'O3_predicted_historico', 'O3_predicted', 'PM10mean_max'
                , 'PM10mean_predicted_historico', 'PM10mean_predicted']]
df = df.sort_values(['fecha'], ascending=[1])

# Diccionario de colores para cada contaminante
dic_colores = {'O3_predicted': '#a50026'
               , 'PM10mean_predicted': '#313695'
               , 'O3_predicted_historico': '#f46d43'
               , 'PM10mean_predicted_historico': '#74add1'
               , 'O3_max': '#d73027'
               , 'PM10mean_max': '#023858'}

# Diccionario de etiquetas para cada contaminante
dic_etiquetas = {'O3_predicted': 'O3 pronóstico'
                 , 'PM10mean_predicted': 'PM10 pronóstico'
                 , 'O3_predicted_historico': 'O3 pronóstico histórico'
                 , 'PM10mean_predicted_historico': 'PM10 pronóstico histórico'
                 , 'O3_max': 'O3 máximo'
                 , 'PM10mean_max': 'PM10 máximo'}


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
                                    value=['O3_max', 'O3_predicted_historico', 'O3_predicted', 'PM10mean_max'
                                           , 'PM10mean_predicted_historico', 'PM10mean_predicted'], multi=True,
                                    placeholder="Contaminantes",  style={'font-family': 'Helvetica',
                                                                         'display': 'inblock-line',
                                                                         'verticalAlign': 'middle',
                                                                         'horizontalAlign': 'right'})]),
                       dcc.Graph(id='pronostico'),
                       html.Div(html.P('** Valores de O3 medidos en micro_gramo/metro cúbico y PM10 en ppb (partículas'
                                       ' por billón)',
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
                                       title='ppb - (micro gramo/metro cúbico)',
                                       dtick=25,
                                       range=[0, 155]),
                                )}


if __name__ == '__main__':
    app.run_server()
