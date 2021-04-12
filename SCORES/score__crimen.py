import pandas as pd
import numpy as np
import Location as lc
import os

path_0 = os.getcwd() + '/'

# RELACIONA LA BASE DE TRAIN
df_train_0 = pd.read_excel(path_0[:-7] + '/Data/df_train_0.xlsx', index_col = 'id')
tabla_3 = df_train_0[['latitud', 'longitud']].copy()

# RELACIONA BASE DE CRIMEN
tabla_1 = pd.read_csv(path_0[:-7] + '/Data/df_crimenupz.csv', index_col = 0)
tabla_1['total_crimen'] = tabla_1.iloc[:,:-2].sum(axis = 1)
tabla_1 = tabla_1[['lat', 'lon', 'total_crimen']]


#----------------------------------------------
# GENERACION DEL SCORE
#----------------------------------------------

tabla_3['SCORE_mean'] = 0.0

for i in range(0, tabla_3.shape[0]):
    print(i, ' / ', tabla_3.shape[0])
    
    # ESTOS CAMPOS PODRIAN CAMBIAR
    lat_ = tabla_3.iloc[i,0]
    lon_ = tabla_3.iloc[i,1]
    
    score_ = lc.Score_crimen(lat_, lon_, tabla_1, 1)
    score_.get_score()
    
    tabla_3.iloc[i, -1] = score_.mean_n
    
    
tabla_3 = tabla_3['SCORE_mean']
tabla_3.to_excel(path_0[:-7] + '/data/scores/score_crimen.xlsx')