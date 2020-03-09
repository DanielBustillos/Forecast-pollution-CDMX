#!/usr/bin/env python
# coding: utf-8

# # Datos entreneamiento Shift O3

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

# In[5]:


import pandas as pd
pd.options.mode.chained_assignment = None 


# In[6]:


path_inicial = "./datos/ingesta_hora_limpios.csv"
path_final = "./datos/ingesta_modelos_O3.csv"


# In[7]:


data_hour_merge_24 = pd.read_csv(path_inicial)


# In[8]:


data_hour_merge_24.head()


# #Quedémonos sin WSR:

# In[9]:


data_hour_merge_24 = data_hour_merge_24[['CO', 'NO', 'NO2', 'NOX', 'O3', 'PM10', "PM2.5",'RH', 'SO2', 'TMP',
       'WSP', 'dia', 'fecha', 'hora', 'id_station', 'mes',"PM10mean","PM25mean"]].reset_index(drop=True)


# #Hagamos una lista con todas las estaciones:

# ### Arreglemos las fechas:

# In[10]:


data_hour_merge_24['dia'] = data_hour_merge_24['dia'].astype(str).astype(float)
data_hour_merge_24['mes'] = data_hour_merge_24['mes'].astype(str).astype(float)


# #Creemos un diccionario con __data_hour_merge_24__ dividido por #estación:

# In[11]:


estaciones = data_hour_merge_24.id_station.unique().tolist()


# In[12]:


data_est = {}
for elem in estaciones:
    data_est[elem] = data_hour_merge_24[data_hour_merge_24.id_station == elem]


# # Leamos el archivo de correlaciones del PM10 mean

# Este archivo se generó en el notebook: __/home/paw/DanielBustillos/contaminación/correlaciones_pau/correlaciones_función_paulina.ipynb__

# In[13]:


target = "O3_y"

O3_corr = pd.read_csv("/DATA/paw/jupyterhub_notebook/daniel.bustillos/DanielBustillos/contaminación/pipeline-norberto/correlacion"+   
                      "/correlaciones_"+ target +".csv")
O3_corr = O3_corr.iloc[:,1:]


# In[14]:


O3_corr.valor.min()


# Vamos a quedarnos con las variables con corr>0.36:

# In[15]:


O3_corr_filtro = O3_corr


# In[16]:


O3_corr_filtro = O3_corr[(O3_corr.valor>0.44) | (O3_corr.valor<-.44) ].reset_index(drop=True)


# Vamos a aplicar el shift para cada elemento de la tabla __O3_corr__:

# In[17]:


def shit_corr(df):
    for i in range(len(O3_corr_filtro)):
        name_column = str( O3_corr_filtro.loc[i,"contaminante"] + "_" + str( O3_corr_filtro.loc[i,"horas"] ) ) 
        df[name_column] = df[O3_corr_filtro.loc[i,"contaminante"]].shift(  int(float(str(O3_corr_filtro.loc[i,"horas"]))) ) 
    return df.dropna()


# Aplicamos esta función para cada DF de cada estación:

# In[18]:


data_shift = {}
for elem in data_est:
    data_shift[elem] = shit_corr(data_est[elem])


# In[19]:


df_append = pd.DataFrame(columns = data_est["MER"].columns.tolist())


# In[20]:


for key in data_est:
    df_append = df_append.append(data_est[key], ignore_index=True,sort=True)


# ## Groupbys

# In[33]:


cols = df_append.columns.tolist()


# In[34]:


#cols.remove("id_station")
cols.remove("fecha")


# Finalmente, aplicamos los groupbys:
#data_hour_merge_24_mean = df_append.groupby(['fecha']).mean()
#data_hour_merge_24_mean.reset_index(inplace=True)#data_hour_merge_24_max = df_append.groupby(['fecha']).max()
#data_hour_merge_24_max.reset_index(inplace=True)#data_hour_merge_24_min = df_append.groupby(['fecha']).min()
#data_hour_merge_24_min.reset_index(inplace=True)
# In[35]:


data_hour_merge_24_mean = df_append.groupby('fecha')[cols].mean()
data_hour_merge_24_mean.reset_index(inplace=True)


# In[36]:


data_hour_merge_24_max = df_append.groupby('fecha')[cols].max()
data_hour_merge_24_max.reset_index(inplace=True)


# In[37]:


data_hour_merge_24_min = df_append.groupby('fecha')[cols].min()
data_hour_merge_24_min.reset_index(inplace=True)


# ### Arreglemos los nombres:

# In[38]:


max_columns = data_hour_merge_24_max.columns.tolist()
min_columns = data_hour_merge_24_min.columns.tolist()
mean_columns = data_hour_merge_24_mean.columns.tolist()


# In[39]:


for i in range(len(max_columns)):
    if max_columns[i] not in ['fecha','hora','dia','mes','id_station']:
        max_columns[i] = max_columns[i]+"_max"
        min_columns[i] = min_columns[i]+"_min"    
        mean_columns[i] = mean_columns[i]+"_mean"


# In[40]:


data_hour_merge_24_mean.columns = mean_columns
data_hour_merge_24_min.columns = min_columns
data_hour_merge_24_max.columns = max_columns


# In[41]:


data_hour_merge_24_max.head()


# ##### Unamos los df's de manera que tengamos en una solo los datos promedio, máximo y minimo por día:

# In[42]:


data_hour_merge = pd.merge(data_hour_merge_24_mean, data_hour_merge_24_max, on=['fecha'])
data_hour_merge = pd.merge(data_hour_merge, data_hour_merge_24_min, on=['fecha'])
data_hour_merge = data_hour_merge.sort_values(['fecha',"hora_x"], ascending=[0,1])


# In[43]:


data_hour_merge.head(48)


# ## Correlacionados con el target.

# Ahora vamos a sacar los atributos más correlacionado con el target, el target es la columna a pronosticar, por simplicidad solo vamos a sacar la correlación con target a las 12 horas:

# Generemos los target de pronóstico:

# Filtremos el DF con las variables mas correlacionadas:

# # agregar 'fecha'

# In[44]:


O3_corr = ['O3_47.0_max',  'TMP_45.0_mean',  'O3_2.0_mean',  'RH_45.0_mean',  'RH_2.0_mean',  'RH_25.0_min',  'O3_23.0_mean',  'RH_44.0_min',  'RH_25.0_mean',  'RH_23.0_max',  'TMP_46.0_mean',  'O3_26.0_mean',  'RH_21.0_max',  'O3_23.0_min',  'TMP_mean',  'O3_22.0_max',  'RH_0.0_min',  'TMP_2.0_min',  'O3_21.0_mean',  'O3_45.0_min',  'hora_35.0_mean',  'NOX_8.0_mean',  'RH_3.0_max',  'hora_20.0_mean',  'TMP_47.0_mean',  'RH_44.0_mean',  'O3_1.0_max',  'NO_7.0_mean',  'RH_46.0_max',  'RH_46.0_mean',  'hora_19.0_mean',  'NO_8.0_max',  'O3_22.0_mean',  'hora_44.0_mean',  'TMP_22.0_max',  'hora_11.0_mean',  'O3_21.0_min',  'O3_25.0_max',  'RH_26.0_mean',  'O3_48.0_mean',  'TMP_21.0_max',  'O3_21.0_max',  'O3_46.0_max',  'TMP_21.0_mean',  'RH_45.0_min',  'RH_24.0_min',  'RH_22.0_mean',  'hora_10.0',  'RH_24.0_mean',  'NOX_7.0_max',  'NOX_7.0_mean',  'O3_25.0_mean',  'TMP_47.0_max',  'TMP_1.0_mean',  'hora_10.0_min',  'O3_3.0_max',  'O3_0.0_mean',  'RH_22.0_max',  'O3_45.0_mean',  'RH_22.0_min',  'RH_48.0_max',  'TMP_25.0_max',  'O3_0.0_min',  'RH_26.0_max',  'hora_34.0_mean',  'RH_min',  'TMP_0.0_max',  'O3_0.0_max',  'O3_46.0_min',  'TMP_22.0_mean',  'O3_45.0_max',  'RH_23.0_min',  'hora_10.0_max',  'O3_24.0_min',  'hora_11.0_min',  'RH_mean',  'TMP_24.0_mean',  'O3_min',  'TMP_48.0_mean',  'O3_46.0_mean',  'TMP_2.0_mean',  'TMP_max',  'PM2.5_3.0_mean',  'O3_20.0_max',  'TMP_23.0_max',  'RH_23.0_mean',  'TMP_25.0_mean',  'O3_24.0_max',  'hora_43.0_mean',  'RH_1.0_max',  'RH_21.0_min',  'RH_25.0_max',  'NO_8.0_mean',  'RH_24.0_max',  'TMP_0.0_min',  'O3_25.0_min',  'hora_33.0_mean',  'hora_21.0_mean',  'TMP_45.0_max',  'RH_2.0_max',  'NOX_8.0_max',  'O3_1.0_mean',  'TMP_min',  'RH_1.0_min',  'TMP_23.0_mean',  'TMP_23.0_min',  'O3_23.0_max',  'TMP_46.0_max',  'TMP_1.0_min',  'O3_3.0_mean',  'O3_2.0_max',  'RH_1.0_mean',  'RH_47.0_max',  'NO_7.0_max',  'RH_2.0_min',  'O3_44.0_mean',  'RH_0.0_mean',  'O3_1.0_min',  'O3_mean',  'RH_21.0_mean',  'RH_max',  'O3_max',  'O3_44.0_max',  'TMP_2.0_max',  'TMP_1.0_max',  'RH_45.0_max',  'TMP_24.0_max',  'RH_47.0_mean',  'O3_22.0_min',  'O3_47.0_min',  'hora_9.0_mean',  'NOX_6.0_mean',  'TMP_0.0_mean',  'O3_2.0_min',  'RH_46.0_min',  'RH_47.0_min',  'hora_9.0_max',  'O3_24.0_mean',  'RH_0.0_max',  'O3_47.0_mean',  'hora_12.0_mean',  'RH_48.0_mean',  'RH_mean_frcst_1',  'RH_mean_frcst_2',  'RH_mean_frcst_3',  'RH_mean_frcst_21',  'RH_mean_frcst_22',  'RH_mean_frcst_23',  'RH_mean_frcst_24',  'WSP_mean_frcst_2',  'WSP_mean_frcst_3',  'WSP_mean_frcst_13',  'WSP_mean_frcst_14',  'WSP_mean_frcst_15',  'WSP_mean_frcst_16',  'TMP_mean_frcst_1',  'TMP_mean_frcst_2',  'TMP_mean_frcst_3',  'TMP_mean_frcst_21',  'TMP_mean_frcst_22',  'TMP_mean_frcst_23',  'TMP_mean_frcst_24']
O3_corr.append("fecha")


# Añadamos los datos de pronostico de las siguientes variables:

# In[45]:


lista_frcst = ["RH_mean","WSP_mean","TMP_mean"]


# In[46]:


for item in lista_frcst:
    for i in range(1, 25):
        col_name = str(item+"_frcst_"+str(i))
        data_hour_merge[col_name] = data_hour_merge[item].shift(i)


# In[51]:


data_hour_merge = data_hour_merge[O3_corr]


# In[52]:


data_hour_merge = data_hour_merge.head(54)
#data_hour_merge = data_hour_merge.fillna(data_hour_merge.mean())


# Guardemos:

# In[53]:


data_hour_merge.to_csv(path_final,sep=',', encoding='utf-8',index=False)

