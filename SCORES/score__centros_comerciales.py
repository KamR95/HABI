import pandas as pd
import numpy as np
import Location as lc
import os
import requests as req
from bs4 import BeautifulSoup
import re
import itertools

path_0 = os.getcwd()

# SE OBTIENE LA INFORMACION DE LOS CENTROS COMERCIALES DE WIKIPEDIA, DESPUES SE OBTIEN LAS COORDENADAS

def get_cc ():
    html = req.get("https://es.wikipedia.org/wiki/Categor%C3%ADa:Centros_comerciales_de_Bogot%C3%A1")
    html_parsed = BeautifulSoup(html.content, 'lxml')
    data = html_parsed.find("div",attrs={"class":"mw-category"})
    a = re.split("[A-Z]+\n",data.text)
    cc = [re.split("\n",a[i]) for i in range(len(a))] [1:]
    cc = list(itertools.chain(*cc))
    return cc

c =  lc.Location()

tabla_1 = []
for i in get_cc():
    c.get_location(i + ", Bogota Cundinamarca")
    tabla_1.append([i, c.latitude, c.longitude])

tabla_1 = pd.DataFrame(tabla_1,columns=["cc", "lat", "lon"])


# SE LLAMA LA BASE df_train_0
df_train_0 = pd.read_excel(path_0[:-6] + '/Data/df_train_0.xlsx', index_col=('id'))


#----------------------------------------------
# GENERACION DEL SCORE
#----------------------------------------------
df_train_0 = df_train_0[['latitud', 'longitud']]
#----------------------------------------------

df_train_0['SCORE_sum'] = 0.0


for i in range(0, df_train_0.shape[0]):
    print(i, ' / ', df_train_0.shape[0])
    
    # ESTOS CAMPOS PODRIAN CAMBIAR
    lat_ = df_train_0.iloc[i,0]
    lon_ = df_train_0.iloc[i,1]
    
    score_ = lc.Score_centros_comerciales(lat_, lon_, tabla_1, 20, 1)
    score_.get_score()
    
    df_train_0.iloc[i, -1] = score_.sum_n

df_train_0 = df_train_0['SCORE_sum']
df_train_0.to_excel(path_0[:-6] + '/Data/scores/score_centro_comercial.xlsx')
