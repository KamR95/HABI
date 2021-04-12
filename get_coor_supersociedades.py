import pandas as pd
import numpy as np
import time
import MODULOS.Location


tabla_1 = pd.read_excel('C:/Users/HP/OneDrive/Documentos/HABIT/SUPERSO/CONSOLIDADO.xlsx')
tabla_1 = tabla_1[tabla_1['Departamento de la dirección de notificación judicial'] == 'BOGOTA D.C.']
tabla_1 = tabla_1[['Codigo Instancia', 'Dirección del domicilio']]
tabla_1['latitud'] = 0.0
tabla_1['longitud'] = 0.0

coor = Location.Location()

for i in range(0, tabla_1.shape[0]):
    
    coor.get_location(str(tabla_1.iloc[i,1]) + ', Bogota, CO')
    
    print('consulta:', i, ' / ', tabla_1.shape[0], '-----> ', coor.latitude, coor.longitude)
    
    tabla_1.iloc[i,2] = coor.latitude
    tabla_1.iloc[i,3] = coor.longitude

#tabla_1.to_excel('C:/Users/HP/OneDrive/Documentos/HABIT/TABLA_1.xlsx')

tabla_2 = tabla_1[(tabla_1['latitud'] < 4.8) & 
                  (tabla_1['latitud'] > 4.4) & 
                  (tabla_1['longitud'] > -75) &
                  (tabla_1['longitud'] < -74)]

tabla_2.to_excel('C:/Users/HP/OneDrive/Documentos/HABIT/Data/df_coodenadas_supersociedades.xlsx')

#plt.scatter(tabla_2['longitud'], tabla_2['latitud'])
