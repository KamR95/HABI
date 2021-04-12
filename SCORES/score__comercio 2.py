import pandas as pd
import numpy as np
import Location as lc
import os

path_1 = os.getcwd() + '/'

# RELACIONA LA BASE DE TRAIN
df_train_0 = pd.read_excel(path_1[:-7] + '/Data/df_train_0.xlsx', index_col = 'id')
tabla_3 = df_train_0[['latitud', 'longitud']].copy()

# RELACIONA BASE DE SS CON COORDENADAS
tabla_1 = pd.read_excel(path_1[:-7] + '/Data/df_coodenadas_supersociedades.xlsx', index_col= 'Codigo Instancia')
tabla_1.drop([tabla_1.columns[0]], axis = 1, inplace = True)

# RELACIONA BASE DE SS
tabla_2 = pd.read_excel(path_1[:-7] + 'Supersociedades/base_supersociedades_seg.xlsx', index_col= 'Codigo Instancia')

# JOINT DE SS COORDENADAS CON LA SS GENERAL
tabla_2['LATITUD'] = tabla_1[tabla_1.columns[-2]]
tabla_2['LONGITUD'] = tabla_1[tabla_1.columns[-1]]

tabla_2 = tabla_2[(tabla_2['LATITUD'] != 0) & (tabla_2['LONGITUD'] != 0)]

# RELACIONA EL CODIGO CIIU
tabla_4 = pd.read_excel(path_1[:-7] + 'Supersociedades/CIIU.xlsx')

# GENERACION DE SS CON COORDENADAS Y SCORE DE CERCANIA
tabla_5 = pd.merge(tabla_2, tabla_4, on=[tabla_2.columns[8]])
tabla_5 = tabla_5.iloc[:,-3:]


#----------------------------------------------
# GENERACION DEL SCORE
#----------------------------------------------

tabla_3['SCORE_sum_positiva'] = 0.0
tabla_3['SCORE_sum_negativa'] = 0.0

for i in range(0, tabla_3.shape[0]):
    print(i, ' / ', tabla_3.shape[0])
    
    # ESTOS CAMPOS PODRIAN CAMBIAR
    lat_ = tabla_3.iloc[i,0]
    lon_ = tabla_3.iloc[i,1]
    
    score_ = lc.Score_comercio(lat_, lon_, tabla_5, 0.6)
    score_.get_score()
    
    tabla_3.iloc[i, -2] = score_.sum_positiva
    tabla_3.iloc[i, -1] = score_.sum_negativa
    
    
tabla_3 = tabla_3[['SCORE_sum_positiva', 'SCORE_sum_negativa']]
tabla_3.to_excel(path_1[:-7] + '/Data/scores/score_comercio_600mm.xlsx')
