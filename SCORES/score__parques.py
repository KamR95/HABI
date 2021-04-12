import pandas as pd
import numpy as np
import Location as lc
import os

path_0 = os.getcwd() + '/'

# RELACIONA LA BASE DE TRAIN
df_train_0 = pd.read_excel(path_0[:-7] + '/Data/df_train_0.xlsx', index_col = 'id')
tabla_3 = df_train_0[['latitud', 'longitud']].copy()

# RELACIONA BASE DE ESTACIONES
tabla_1 = pd.read_excel(path_0[:-7] + '/Data/parques_zon_met.xlsx', index_col = 0 )

#----------------------------------------------
# GENERACION DEL SCORE
#----------------------------------------------

tabla_3['SCORE_suma'] = 0.0

for i in range(0, tabla_3.shape[0]):
    print(i, ' / ', tabla_3.shape[0])
    
    # ESTOS CAMPOS PODRIAN CAMBIAR
    lat_ = tabla_3.iloc[i,0]
    lon_ = tabla_3.iloc[i,1]
    
    score_ = lc.Score_parques(lat_, lon_, tabla_1, 0.3)
    score_.get_score()
    
    tabla_3.iloc[i, -1] = score_.sum_n
    

tabla_3 = tabla_3['SCORE_suma']
tabla_3.to_excel(path_0[:-7] + '/data/scores/score_parques_zon_met.xlsx')
