import pandas as pd
import numpy as np
import os
import MODULOS.Location as lc


path_0 = os.getcwd()
tabla_1 = pd.read_excel(path_0 + '/Data/df_train_0.xlsx', index_col = 'id' )
tabla_1 = tabla_1[['latitud', 'longitud', 'valormetrocuadrado']]
tabla_1['sesgo'] = 0.0

tabla_3 = tabla_1.copy()

tabla_2 = pd.read_excel(path_0 + '/Data/Scores/score_catastro.xlsx', index_col = 'id')
tabla_2.columns = ['score_catastro']
tabla_2[tabla_2['score_catastro'] == 0] = tabla_2[tabla_2!=0].min()[0] # MINIMO

tabla_1['score_catastro'] = tabla_2

modelo_factores = 0.06 # FACTOR MODEL

#for i in range(0, 10):
for i in range(0, tabla_1.shape[0]):
    #break
    
    # VALIDADOR PRECIO LAST CONTRA PRECIO CATASTRO
    if tabla_1.iloc[i, 2] < tabla_1.iloc[i, 4]: continue
    
    # ESTOS CAMPOS PODRIAN CAMBIAR
    lat_ = tabla_1.iloc[i,0]
    lon_ = tabla_1.iloc[i,1]
    
    score_ = lc.Prima_df(lat_, lon_, tabla_1, 0.3)
    score_.get_score()
    
    df_ = score_.df.copy()
    df_[df_['dist_rel'] == 1.0]
    
    if df_.shape[0] == 0: continue
    
    df_['valormetrocuadrado_val']  = df_['valormetrocuadrado'] 
    
    for u in range(100):
        
        df_['sesgo_val'] = list(np.random.uniform(low = - modelo_factores , high = 0, size = df_.shape[0]))
        df_['Y_prima'] = df_['valormetrocuadrado'] * ( 1 + df_['sesgo_val'])

        if df_['Y_prima'].std() < df_['valormetrocuadrado_val'].std():
            
            df_['sesgo'] = df_['sesgo_val'] 
            df_['valormetrocuadrado_val'] = df_['valormetrocuadrado'] * ( 1 + df_['sesgo_val'])
            
            #print((df_['valormetrocuadrado'] * ( 1 + df_['sesgo'])).std())

    tabla_1.update(df_['sesgo'])
    
    print(i, ' / ', tabla_1.shape[0])
    
    

tabla_1['valormetrocuadrado'] = tabla_1['valormetrocuadrado'] * (1 + tabla_1['sesgo'])
tabla_1 = tabla_1['valormetrocuadrado']
tabla_1.to_excel(path_0 + '/Data/df_Y_prima_train.xlsx')

