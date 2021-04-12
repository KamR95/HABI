import pandas as pd
import numpy as np
import Location as lc
import os

path_0 = os.getcwd() + '/'

# RELACIONA LA BASE DE TRAIN
df_train_0 = pd.read_excel(path_0[:-13] + '/Data/df_test_0.xlsx', index_col = 'id')
tabla_3 = df_train_0[['latitud', 'longitud']].copy()

# RELACIONA BASE DE PLAZAS DE MERCADO
# ESTA INFORMACION SE DESCARGA DEL SIGUIENTE LINK: https://datosabiertos.bogota.gov.co/dataset/plazas-de-mercado-distritales
tabla_1 = pd.read_excel(path_0[:-13] + "\\Data\\plazas-de-mercado.xlsx")
tabla_1 = tabla_1[["Nombre","coord_y","coord_x"]]

#----------------------------------------------
# GENERACION DEL SCORE
#----------------------------------------------

tabla_3['SCORE_suma'] = 0.0

for i in range(0, tabla_3.shape[0]):
    print(i, ' / ', tabla_3.shape[0])
    
    # ESTOS CAMPOS PODRIAN CAMBIAR
    lat_ = tabla_3.iloc[i,0]
    lon_ = tabla_3.iloc[i,1]
    
    score_ = lc.Score_plaza(lat_, lon_, tabla_1, 0.3)
    score_.get_score()
    
    tabla_3.iloc[i, -1] = score_.sum_n
    

tabla_3 = tabla_3['SCORE_suma']
tabla_3.to_excel(path_0[:-13] + '/data/scores_test/score_plazas-de-mercado.xlsx')
