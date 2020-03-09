#!/usr/bin/env python
# coding: utf-8

# # Datos entreneamiento Shift PM10

# En este notebook vamos a aplicar el shift para las obtener las columnas mas correlacionadas.
# 
# - __Datos recibidos:__ obtenidos de notebook __1-datos_entrenamiento_shift.ipynb__
# - __Responsable:__ Daniel Bustillos
# - __Contacto:__  juandaniel.bucam@gmail.com
# 
# __Notas del proyecto__
# Necesitamos generar un csv con los niveles máximos, mínimo y promedio por día, se perderá la información de la estación, también generaremos el atributo PM10mean y PM25mean que representarán los valores de las últimas 24 horas de los contaminantes.
# 
# calidad de caire
# pronostico contaminación

# ## Pasos
# [X] Aplicar Shift con Correlaciones <br>
# [X] Sacar minimo promedio y maximo <br>
# [X] Obtener columnas más correlacionadas<br><br>

# In[1]:


import pandas as pd
pd.options.mode.chained_assignment = None 


# In[2]:


path_inicial = "./datos/ingesta_hora_limpios.csv"
path_final = "./datos/ingesta_modelos_PM10.csv"


# In[3]:


data_hour_merge_24 = pd.read_csv(path_inicial)


# In[4]:


data_hour_merge_24.head()


# Quedémonos sin WSR:

# In[5]:


data_hour_merge_24 = data_hour_merge_24[['CO', 'NO', 'NO2', 'NOX', 'O3', 'PM10', "PM2.5",'RH', 'SO2', 'TMP',
       'WSP', 'dia', 'fecha', 'hora', 'id_station', 'mes',"PM10mean","PM25mean"]].reset_index(drop=True)


# Hagamos una lista con todas las estaciones:

# ### Arreglemos las fechas:

# In[6]:


data_hour_merge_24['dia'] = data_hour_merge_24['dia'].astype(str).astype(float)
data_hour_merge_24['mes'] = data_hour_merge_24['mes'].astype(str).astype(float)


# In[7]:


estaciones = data_hour_merge_24.id_station.unique().tolist()


# In[8]:


data_est = {}
for elem in estaciones:
    data_est[elem] = data_hour_merge_24[data_hour_merge_24.id_station == elem]


# # Leamos el archivo de correlaciones del PM10 mean

# Este archivo se generó en el notebook: __/home/paw/DanielBustillos/contaminación/correlaciones_pau/correlaciones_función_paulina.ipynb__

# In[9]:


target = "PM10mean_y"

O3_corr = pd.read_csv("/DATA/paw/jupyterhub_notebook/daniel.bustillos/DanielBustillos/contaminación/pipeline-norberto/correlacion"+
                      "/correlaciones_"+ target +".csv")
O3_corr = O3_corr.iloc[:,1:]
print("target = PM10mean_y")

# In[10]:


O3_corr.valor.min()


# Vamos a quedarnos con las variables con corr>0.66:

# In[11]:


O3_corr_filtro = O3_corr


# In[12]:


O3_corr_filtro = O3_corr[(O3_corr.valor>0.46) | (O3_corr.valor<-0.46) ].reset_index(drop=True)


# Vamos a aplicar el shift para cada elemento de la tabla __O3_corr__:

# In[13]:


def shit_corr(df):
    for i in range(len(O3_corr_filtro)):
        name_column = str( O3_corr_filtro.loc[i,"contaminante"] + "_" + str( O3_corr_filtro.loc[i,"horas"] ) ) 
        df[name_column] = df[O3_corr_filtro.loc[i,"contaminante"]].shift( int(float(str(O3_corr_filtro.loc[i,"horas"]))) ) 
    return df.dropna()


# Aplicamos esta función para cada DF de cada estación:

# In[14]:


data_shift = {}
for elem in data_est:
    data_shift[elem] = shit_corr(data_est[elem])


# In[15]:


df_append = pd.DataFrame(columns = data_est["MER"].columns.tolist())


# In[16]:


for key in data_est:
    df_append = df_append.append(data_est[key], ignore_index=True,sort=True)


# In[17]:


df_append.columns.tolist()


# In[18]:


df_append['fecha'] =  pd.to_datetime(df_append['fecha'], format='%Y-%m-%d %H:%M')

import matplotlib.pyplot as plt



# ## Groupbys

# In[19]:


cols = df_append.columns.tolist()


# In[20]:


#cols.remove("id_station")
cols.remove("fecha")


# Finalmente, aplicamos los groupbys:

# In[21]:
print("remove")


data_hour_merge_24_mean = df_append.groupby('fecha')[cols].mean()
data_hour_merge_24_mean.reset_index(inplace=True)

print("mean")
# In[22]:


data_hour_merge_24_max = df_append.groupby('fecha')[cols].max()
data_hour_merge_24_max.reset_index(inplace=True)
print("nmax")

# In[23]:


data_hour_merge_24_min = df_append.groupby('fecha')[cols].min()
data_hour_merge_24_min.reset_index(inplace=True)
print("min")

# ### Arreglemos los nombres:

# In[24]:


max_columns = data_hour_merge_24_max.columns.tolist()
min_columns = data_hour_merge_24_min.columns.tolist()
mean_columns = data_hour_merge_24_mean.columns.tolist()


# In[25]:


for i in range(len(max_columns)):
    if max_columns[i] not in ['fecha','hora','dia','mes','id_station']:
        max_columns[i] = max_columns[i]+"_max"
        min_columns[i] = min_columns[i]+"_min"    
        mean_columns[i] = mean_columns[i]+"_mean"


# In[26]:


data_hour_merge_24_mean.columns = mean_columns
data_hour_merge_24_min.columns = min_columns
data_hour_merge_24_max.columns = max_columns


# In[27]:


data_hour_merge_24_max.head()


# ##### Unamos los df's de manera que tengamos en una solo los datos promedio, máximo y minimo por día:

# In[52]:


data_hour_merge = pd.merge(data_hour_merge_24_mean, data_hour_merge_24_max, on=['fecha'])
data_hour_merge = pd.merge(data_hour_merge, data_hour_merge_24_min, on=['fecha'])
data_hour_merge = data_hour_merge.sort_values(['fecha',"hora_x"], ascending=[0,1])

print("ascending")
# In[53]:


data_hour_merge.head()


# ## Correlacionados con el target.

# Ahora vamos a sacar los atributos más correlacionado con el target, el target es la columna a pronosticar, por simplicidad solo vamos a sacar la correlación con target a las 12 horas:

# Generemos los target de pronóstico:

# Filtremos el DF con las variables mas correlacionadas:

# In[54]:


O3_corr = ['PM10mean_1.0_max',  'PM10_9.0_mean',  'PM10_max',  'PM10_6.0_mean',  'PM10mean_4.0_mean',  'PM25mean_8.0_max',  'PM10mean_2.0_max',  'PM25mean_0.0_mean',  'PM10mean_11.0_mean',  'PM10mean_13.0_mean',  'PM10_2.0_mean',  'PM10_13.0_mean',  'PM10_3.0_mean',  'PM10mean_28.0_max',  'PM25mean_1.0_max',  'PM10mean_26.0_mean',  'PM10mean_10.0_mean',  'PM10mean_7.0_mean',  'PM10mean_16.0_mean',  'PM10mean_20.0_mean',  'PM10mean_4.0_max',  'PM10mean_29.0_max',  'PM10mean_5.0_max',  'PM25mean_2.0_max',  'PM25mean_5.0_mean',  'PM10mean_9.0_max',  'PM25mean_4.0_max',  'PM10mean_19.0_max',  'PM25mean_4.0_mean',  'PM10mean_10.0_max',  'PM2.5_mean',  'PM25mean_max',  'PM10_7.0_max',  'PM10_7.0_mean',  'PM25mean_12.0_max',  'PM10mean_24.0_max',  'PM10_8.0_max',  'PM10mean_25.0_mean',  'PM10_3.0_max',  'PM10mean_14.0_max',  'PM10mean_30.0_mean',  'PM25mean_13.0_max',  'PM10_0.0_mean',  'PM10mean_24.0_mean',  'PM10mean_max',  'PM10mean_25.0_max',  'PM10_6.0_max',  'PM10mean_23.0_max',  'PM25mean_3.0_max',  'PM25mean_0.0_max',  'PM10mean_5.0_mean',  'PM10_14.0_mean',  'PM10mean_14.0_mean',  'PM10mean_18.0_max',  'PM25mean_3.0_mean',  'PM10mean_31.0_mean',  'PM10mean_26.0_max',  'PM25mean_6.0_max',  'PM10mean_9.0_mean',  'PM10mean_22.0_mean',  'PM25mean_2.0_mean',  'PM10mean_11.0_max',  'PM10_16.0_mean',  'PM10mean_mean',  'PM25mean_1.0_mean',  'PM10_10.0_mean',  'PM10_1.0_mean',  'PM10mean_22.0_max',  'PM10mean_27.0_max',  'PM10mean_12.0_max',  'PM25mean_5.0_max',  'PM10mean_21.0_max',  'PM10_5.0_mean',  'PM10mean_0.0_max',  'PM10_4.0_mean',  'PM25mean_9.0_max',  'PM10mean_17.0_max',  'PM10mean_18.0_mean',  'PM10mean_28.0_mean',  'PM10_1.0_max',  'PM10_4.0_max',  'PM10mean_17.0_mean',  'NO2_mean',  'PM25mean_mean',  'PM10mean_0.0_mean',  'PM10_2.0_max',  'PM10mean_6.0_mean',  'PM25mean_10.0_max',  'PM10mean_20.0_max',  'PM10mean_19.0_mean',  'PM10mean_29.0_mean',  'PM10_15.0_mean',  'PM10mean_1.0_mean',  'PM10mean_3.0_max',  'PM25mean_7.0_max',  'PM25mean_11.0_max',  'PM10mean_8.0_max',  'PM10_0.0_max',  'PM10mean_16.0_max',  'PM10mean_13.0_max',  'PM10_5.0_max',  'PM10_11.0_mean',  'PM10mean_15.0_mean',  'PM10mean_23.0_mean',  'PM10mean_27.0_mean',  'PM10mean_8.0_mean',  'PM10mean_2.0_mean',  'PM10mean_12.0_mean',  'PM10_8.0_mean',  'PM10mean_21.0_mean',  'PM10_12.0_mean',  'PM10mean_15.0_max',  'PM10_mean',  'PM10mean_6.0_max',  'PM10mean_3.0_mean',  'PM10mean_7.0_max']


# In[55]:

print("append")
O3_corr.append("fecha")


# Añadamos los datos de pronostico de las siguientes variables:

# In[56]:


lista_frcst = ["RH_mean","WSP_mean","TMP_mean"]


# In[57]:


for item in lista_frcst:
    for i in range(1, 25):
        col_name = str(item+"_frcst_"+str(i))
        data_hour_merge[col_name] = data_hour_merge[item].shift(i)


# In[58]:


data_hour_merge = data_hour_merge[O3_corr]
print("filtro")

# In[59]:


data_hour_merge.head()


# In[60]:


data_hour_merge = data_hour_merge.head(54)
#data_hour_merge = data_hour_merge.fillna(data_hour_merge.mean())


# In[61]:


data_hour_merge.head()


# Guardemos:

# In[62]:


data_hour_merge.to_csv(path_final,sep=',', encoding='utf-8',index=False)



