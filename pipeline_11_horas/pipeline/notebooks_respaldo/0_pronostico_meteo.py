
# coding: utf-8

# In[1]:


import datetime
import time
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'


# In[2]:


url = "https://www.tutiempo.net/mexico-d-f.html?datos=por-horas&v=list"


# In[3]:


df = pd.read_html(url)
df = df[3]


# In[4]:


df.rename(columns={0: 'hora', 2: 'TMP',3:"WSP",5:"RH"}, inplace=True)
df.drop([1,4,6],axis=1,inplace=True)


# In[5]:


df["hora"] = df["hora"].str[0:2]


# In[6]:


index_next = df.index.get_indexer_for(df[df.hora=='Ma'].index)


# In[7]:


now = datetime.datetime.now()
df_hoy = df.iloc[2:index_next[0]]
#df_hoy.columns = df.iloc[1,:].values.tolist()
df_hoy["fecha"] = str( str(now.year) + "-" + str(now.month) + "-" + str(now.day) + " " )# + df_hoy["Hora"]
df_hoy["fecha"] = pd.to_datetime(df_hoy["fecha"])
df_hoy.reset_index(inplace=True,drop=True)


# In[8]:


df_manana =  df.iloc[index_next[0]+2:index_next[0]+2+24]
df_manana["fecha"] = df_hoy.loc[1,"fecha"] + pd.to_timedelta(1, unit='d')


# In[9]:


df_prono = pd.concat([df_hoy, df_manana], ignore_index=True)
df_prono["TMP"] = df_prono["TMP"].str[0:2]
df_prono["RH"] = df_prono["RH"].str.split('%').str[0]
df_prono["WSP"] = df_prono["WSP"].str[0:2]
df_prono['fecha'] = df_prono['fecha'].astype(str)
df_prono["mes"] = df_prono["fecha"].str[5:7]
df_prono["dia"] = df_prono["fecha"].str[8:10]

df_prono.to_csv("/home/paw/DanielBustillos/ingesta280519/pronostico_meteo.csv", sep=',', index=False)
# In[10]:


df_prono

