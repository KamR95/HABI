import pandas as pd
import numpy as np
import Location as lc
import os

path_0 = os.getcwd() + '/'

# RELACIONA LA BASE DE TRAIN
df_train_0 = pd.read_excel(path_0[:-7] + '/Data/df_train_0.xlsx', index_col = 'id')
tabla_3 = df_train_0[['latitud', 'longitud']].copy()

# RELACIONA BASE DE CARCELES
tabla_1 = pd.read_csv('https://bogota-laburbano.opendatasoft.com/explore/dataset/carcel/download/?format=csv&timezone=America/Bogota&lang=es&use_labels_for_header=true&csv_separator=%3B', delimiter=';')
tabla_1 = tabla_1[['Nombre', 'geo_point_2d']]
tabla_1[['lat', 'lon']] = tabla_1['geo_point_2d'].str.split(',', expand = True)
tabla_1.drop(['geo_point_2d'], axis = 1, inplace = True)

#----------------------------------------------
# GENERACION DEL SCORE
#----------------------------------------------

tabla_3['SCORE_suma'] = 0.0

for i in range(0, tabla_3.shape[0]):
    print(i, ' / ', tabla_3.shape[0])
    
    # ESTOS CAMPOS PODRIAN CAMBIAR
    lat_ = tabla_3.iloc[i,0]
    lon_ = tabla_3.iloc[i,1]
    
    score_ = lc.Score_carceles(lat_, lon_, tabla_1, 0.5)
    score_.get_score()
    
    tabla_3.iloc[i, -1] = score_.sum_n
    

tabla_3 = tabla_3['SCORE_suma']
tabla_3.to_excel(path_0[:-7] + '/data/scores/score_carceles.xlsx')
