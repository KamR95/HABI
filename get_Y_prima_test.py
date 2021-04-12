import pandas as pd
import numpy as np
import os
import MODULOS.Location as lc

path_0 = os.getcwd()

# TRAIN

tabla_1_train = pd.read_excel(path_0 + '/Data/df_train_0.xlsx', index_col = 'id' )
tabla_1_train = tabla_1_train[['latitud', 'longitud', 'valormetrocuadrado']]
tabla_1_train['sesgo'] = 0.0

tabla_3_train = tabla_1_train.copy()

tabla_2_train = pd.read_excel(path_0 + '/Data/Scores/score_catastro.xlsx', index_col = 'id')
tabla_2_train.columns = ['score_catastro']
tabla_2_train[tabla_2_train['score_catastro'] == 0] = tabla_2_train[tabla_2_train!=0].min()[0] # MINIMO

tabla_1_train['score_catastro'] = tabla_2_train

# TEST

tabla_1_test = pd.read_excel(path_0 + '/Data/df_test_0.xlsx', index_col = 'id' )
tabla_1_test = tabla_1_test[['latitud', 'longitud', 'valormetrocuadrado']]
tabla_1_test['sesgo'] = 0.0

tabla_3 = tabla_1_test.copy()

tabla_2_test = pd.read_excel(path_0 + '/Data/Scores_test/score_catastro.xlsx', index_col = 'id')
tabla_2_test.columns = ['score_catastro']
tabla_2_test[tabla_2_test['score_catastro'] == 0] = tabla_2_test[tabla_2_test!=0].min()[0] # MINIMO

tabla_1_test['score_catastro'] = tabla_2_test

modelo_factores = 0.06 # FACTOR MODEL

tabla_1 = tabla_1_train.append(tabla_1_test)

#for i in range(0, 10):
for i in range(0, tabla_1_test.shape[0]):
    #break
    
    # VALIDADOR PRECIO LAST CONTRA PRECIO CATASTRO
    if tabla_1_test.iloc[i, 2] < tabla_1_test.iloc[i, 4]: continue
    
    # ESTOS CAMPOS PODRIAN CAMBIAR
    lat_ = tabla_1_test.iloc[i,0]
    lon_ = tabla_1_test.iloc[i,1]
    
    score_ = lc.Prima_df(lat_, lon_, tabla_1, 0.3)
    score_.get_score()
    
    df_ = score_.df.copy()
    df_[df_['dist_rel'] == 1.0]
    
    if df_.shape[0] == 0: continue
    
    df_['valormetrocuadrado_val']  = df_['valormetrocuadrado'] 
    
    for u in range(100):
        
        df_['sesgo_val'] = list(np.random.uniform(low = -0.05 , high = 0, size = df_.shape[0]))
        df_['Y_prima'] = df_['valormetrocuadrado'] * ( 1 + df_['sesgo_val'])

        if df_['Y_prima'].std() < df_['valormetrocuadrado_val'].std():
            
            df_['sesgo'] = df_['sesgo_val'] 
            df_['valormetrocuadrado_val'] = df_['valormetrocuadrado'] * ( 1 + df_['sesgo_val'])
            
            #print((df_['valormetrocuadrado'] * ( 1 + df_['sesgo'])).std())

    tabla_1.update(df_['sesgo'])
    
    print(i, ' / ', tabla_1_test.shape[0])

tabla_1['valormetrocuadrado'] = tabla_1['valormetrocuadrado'] * (1 + tabla_1['sesgo'])
tabla_1 = tabla_1.loc[tabla_1_test.index]
tabla_1 = tabla_1['valormetrocuadrado']
tabla_1.to_excel(path_0 + '/Data/df_Y_prima_test.xlsx')

