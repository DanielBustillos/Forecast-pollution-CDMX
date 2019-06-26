import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

df_pm25 = pd.read_csv("/home/pradel/Desktop/Forecast_CDMX_pollution/correlacion/sub_dataset/corr_pm25_72.csv")

uva = go.Scatter(
    x=df_pm25['horas'],
    y=df_pm25['UVA'],
    name='UVA',
    line=dict(
        color='#000000',
        width=2)
)
uvb = go.Scatter(
    x=df_pm25['horas'],
    y=df_pm25['UVB'],
    name='UVB',
    line=dict(
        color='#004949',
        width=2)
)
pa = go.Scatter(
    x=df_pm25['horas'],
    y=df_pm25['PA'],
    name='PA',
    line=dict(
        color='#009292',
        width=2)
)
co = go.Scatter(
    x=df_pm25['horas'],
    y=df_pm25['CO'],
    name='CO',
    line=dict(
        color='#ff6db6',
        width=2)
)
no = go.Scatter(
    x=df_pm25['horas'],
    y=df_pm25['NO'],
    name='NO',
    line=dict(
        color='#ffb6db',
        width=2)
)
no2 = go.Scatter(
    x=df_pm25['horas'],
    y=df_pm25['NO2'],
    name='NO2',
    line=dict(
        color='#490092',
        width=2)
)
nox = go.Scatter(
    x=df_pm25['horas'],
    y=df_pm25['NOX'],
    name='NOX',
    line=dict(
        color='#006ddb',
        width=2)
)
o3 = go.Scatter(
    x=df_pm25['horas'],
    y=df_pm25['O3'],
    name='O3',
    line=dict(
        color='#b66dff',
        width=2)
)
pm25 = go.Scatter(
    x=df_pm25['horas'],
    y=df_pm25['PM25'],
    name='PM2.5',
    line=dict(
        color='#6db6ff',
        width=2)
)
pmco = go.Scatter(
    x=df_pm25['horas'],
    y=df_pm25['PMCO'],
    name='PMCO',
    line=dict(
        color='#b6dbff',
        width=2)
)
so2 = go.Scatter(
    x=df_pm25['horas'],
    y=df_pm25['SO2'],
    name='SO2',
    line=dict(
        color='#920000',
        width=2)
)
rh = go.Scatter(
    x=df_pm25['horas'],
    y=df_pm25['RH'],
    name='RH',
    line=dict(
        color='#924900',
        width=2)
)
tmp = go.Scatter(
    x=df_pm25['horas'],
    y=df_pm25['TMP'],
    name='TMP',
    line=dict(
        color='#db6d00',
        width=2)
)
wsp = go.Scatter(
    x=df_pm25['horas'],
    y=df_pm25['WSP'],
    name='WSP',
    line=dict(
        color='#ffff6d',
        width=2)
)
wdr = go.Scatter(
    x=df_pm25['horas'],
    y=df_pm25['WDR'],
    name='WDR',
    line=dict(
        color='#24ff24',
        width=2)
)
pm10 = go.Scatter(
    x=df_pm25['horas'],
    y=df_pm25['PM10'],
    name='PM10',
    line=dict(
        color='rgb(205, 12, 24)',
        width=2)
)

data_pm25 = [uva, uvb, pa, co, no, no2, nox, o3, pm25, pmco, so2, rh, tmp, wsp, wdr, pm10]

app = dash.Dash()

app.layout = html.Div([dcc.Graph(id='contaminantes',
                                 figure={'data': data_pm25,
                                         'layout': go.Layout(title='Correlaciones de PM2.5 con otros contaminantes',
                                                             xaxis={'title': 'Horas'},
                                                             yaxis={'title': 'Partículas por millón'}
                                                             )})])


if __name__ == '__main__':
    app.run_server()