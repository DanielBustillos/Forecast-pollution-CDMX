
# coding: utf-8

# # Arreglar datos

# In[1]:


import pandas as pd
import numpy as np

from functools import reduce
from datetime import datetime
pd.options.mode.chained_assignment = None  # default='warn'
import datetime as dt


# # Corremos el script del pronóstico metereológico

# In[2]:


exec(open("./pronostico_meteo.py").read())


# Leemos el archivo:

# In[3]:


df_pronos = pd.read_csv("./datos/pronostico_meteo.csv")
df_pronos['TMP'] = df_pronos['TMP'].astype(float)
df_pronos['WSP'] = df_pronos['WSP'].astype(float)
df_pronos['RH'] = df_pronos['RH'].astype(float)
df_pronos['TMP'] = df_pronos['TMP'].astype(float)


# In[4]:


df_pronos = df_pronos.reindex(index=df_pronos.index[::-1]).reset_index(drop=True)


# ## Limpiemos los datos de aire.cdmx

# In[5]:


contaminantes = ["so2","co","nox","no2","no","o3","pm10","wsp","wdr","tmp","rh","pm2"]


# In[6]:


def time_converter_date(x):
    x0 = x.split("-")
    return x0[2]+"-"+x0[1]+"-"+x0[0]


# Para restar una hora:

# In[7]:


def time_converter(hora,fecha):
    if hora[:].endswith("24"):
        fecha = str(fecha+" "+str(int(hora)-1)+":00")
        the_time = dt.datetime.strptime(fecha, '%Y-%m-%d %H:%M')
        new_time = the_time + dt.timedelta(hours=1)
        return new_time.strftime('%Y-%m-%d'),new_time.strftime('%H:%M')
    else:
        return  fecha, hora


# #### para automatizar el acceso a la liga de aire.cdmx:

# In[8]:


from datetime import datetime


# In[9]:


anio = str(datetime.today().year)
mes = str(datetime.today().month).zfill(2)
name="O3"


# ## Definimos la función para obtener los datos
str("http://www.aire.cdmx.gob.mx/estadisticas-consultas/concentraciones/"
                          +"respuesta.php?qtipo=HORARIOS&parametro="+name+"&anio="+anio+"&qmes="+mes)
# In[10]:


def dataframe(name):
    df = pd.read_html(str("http://www.aire.cdmx.gob.mx/estadisticas-consultas/concentraciones/"
                          +"respuesta.php?qtipo=HORARIOS&parametro="+name+"&anio="+anio+"&qmes="+mes),skiprows=1)  
    df[0].columns = df[1].values.tolist()[0]
    df[0].drop(0,axis=0,inplace=True)
    df = df[0].replace("nr",np.nan)
    #df=pd.read_csv("path_historico")
    
    df = df.tail(70)
    
    df = pd.melt(df, id_vars=['Fecha', 'Hora'], value_vars=['ACO', 'AJM', 'AJU', 'ATI', 'AZC', 'BJU', 'CAM', 'CCA',
       'CES', 'MON', 'CHO', 'COY', 'CUA', 'CUT', 'FAC', 'FAR', 'GAM', 'HGM',
       'INN', 'IZT', 'LAG', 'LLA', 'LPR', 'MER', 'MGH', 'MPA', 'NEZ', 'PED',
       'PLA', 'SAC', 'SAG', 'SFE', 'SJA', 'SUR', 'TAC', 'TAH', 'TAX', 'TEC',
       'TLA', 'TLI', 'TPN', 'UAX', 'UIZ', 'VIF', 'XAL'])
    
    df["dia"] =  df["Fecha"].str[0:2]
    df["mes"] = df["Fecha"].str[3:5]
    
    #df["Fecha"] = df.apply(lambda row: time_parser(row['Fecha'],row['Hora']), axis=1)
    df["Fecha"] = df.apply(lambda row: time_converter_date(row["Fecha"]), axis=1)
    #print(df["Hora"])
    df["Fecha"] =  df.apply(lambda row: time_converter(row["Hora"],row["Fecha"])[0], axis=1)
    df["Hora"] =  df.apply(lambda row: time_converter(row["Hora"],row["Fecha"])[1], axis=1)
    
    #df["Hora"] = df.apply(lambda row: parser_date(row['Hora']), axis=1)
    df = df.rename(columns = {'variable': 'id_station',"Fecha": "fecha","value":name.upper(),"Hora":"hora"})

    return df


# ### Corremos la función:

# La hora de actualización de lo archivos es: a los 15 minuntos de cada hora

# In[11]:


dic_df = {i:dataframe(i) for i in contaminantes}


# In[12]:


lista = [dic_df['so2'],dic_df['co'],dic_df['nox'],dic_df['no'],dic_df['no2'],dic_df['o3'],dic_df['pm10'],
         dic_df['wsp'],dic_df['wdr'],dic_df['tmp'],dic_df['rh'],dic_df['pm2']]


# ## Junatamos todos los contaminantes

# In[13]:


df_final = reduce(lambda left,right: pd.merge(left,right,on=["fecha",'id_station',"hora","dia","mes"]), lista)


# In[14]:


df_final['O3'] = pd.to_numeric(df_final['O3'], errors='coerce')
df_final['hora'] = pd.to_numeric(df_final['hora'], errors='coerce')
df_final['dia'] = pd.to_numeric(df_final['dia'], errors='coerce')
df_final['mes'] = pd.to_numeric(df_final['mes'], errors='coerce')
df_final['CO'] = pd.to_numeric(df_final['CO'], errors='coerce')
df_final['NOX'] = pd.to_numeric(df_final['NOX'], errors='coerce')
df_final['NO'] = pd.to_numeric(df_final['NO'], errors='coerce')
df_final['PM10'] = pd.to_numeric(df_final['PM10'], errors='coerce')
df_final['WSP'] = pd.to_numeric(df_final['WSP'], errors='coerce')
df_final['WDR'] = pd.to_numeric(df_final['WDR'], errors='coerce')
df_final['TMP'] = pd.to_numeric(df_final['TMP'], errors='coerce')
df_final['RH'] = pd.to_numeric(df_final['RH'], errors='coerce')
df_final['PM2'] = pd.to_numeric(df_final['PM2'], errors='coerce')


# In[15]:


df_final = df_final.rename(columns={'PM2': 'PM2.5'})
df_final["hora"] = df_final.hora.fillna("0")


# Guardamos este archivo por hora **SOLO LA PRIMERA VEZ!!** 

# In[16]:


df_final.to_csv("./datos/ingesta_conta_hora.csv", sep=',', index=False)


# Leemos este mismo archivo, es el pasado!

# In[17]:


df_horas = pd.read_csv("./datos/ingesta_conta_hora.csv")


# concatenamos el archivo que acabamos de generar

# In[18]:


df_merge = df_final.append(df_horas, ignore_index=False,sort=True)


# Lo volvemos a guardar

# In[19]:


df_merge.to_csv("./datos/ingesta_conta_hora.csv", sep=',', index=False)


# ## Hacemos un merge 

# In[20]:


df_final.hora = df_final.hora.astype(int)


# In[21]:


df_all = df_pronos.merge(df_final,  how='outer',on=["fecha","hora","dia","mes","TMP","WSP","RH"])


# In[22]:


df_all = df_all[['CO', 'NO', 'NO2', 'NOX', 'O3', 'PM10', "PM2.5",'RH', 'SO2', 'TMP',
       'WSP', 'dia', 'fecha', 'hora', 'id_station', 'mes',"WDR"]]
df_all["id_station"] = df_all["id_station"].fillna("prono")


# In[23]:


df_all['fecha']  = pd.to_datetime([''.join([' '.join([df_all.loc[i, 'fecha'], 
                                                         str(df_all.loc[i, 'hora'])]),':00']) for i in df_all.index])


# In[24]:


df_all = df_all.sort_values(['fecha','id_station'], ascending=[0, 1])


# In[25]:


df_all.head(32)


# In[26]:


df_all.to_csv("./datos/ingesta_hora.csv", sep=',', index=False)

