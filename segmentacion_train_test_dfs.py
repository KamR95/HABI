import pandas as pd
import os
import MODULOS.Segmentacion as seg

path_0 = os.getcwd()

# GENERACION BASE df_train_0

tabla_1 = pd.read_csv(path_0 + '/Data/train_data.csv')

tabla_2 = seg.Seg_train(tabla_1)
tabla_2.get_segmetacion()

tabla_2.df_train_0.to_excel(path_0 + '/Data/df_train_0.xlsx')

columas_df = list(tabla_2.df_train_0.columns)

# GENERACION BASE df_test_0

tabla_1 = pd.read_csv(path_0 + '/Data/test_data.csv')

tabla_2 = seg.Seg_test(tabla_1, columas_df)
tabla_2.get_segmetacion()

tabla_2.df_test_0.to_excel(path_0 + '/Data/df_test_0.xlsx')

# GENERAR BASE DELIMITADA SUPERSOCIEDADES

tabla_1 = pd.read_excel(path_0 + '/Supersociedades/base_supersociedades.xlsx')

tabla_2 = seg.Seg_superso(tabla_1)
tabla_2.get_segmetacion()

tabla_2.df_segmentada.to_excel(path_0 + '/Supersociedades/base_supersociedades_seg.xlsx')

Index(['balcon', 'banos', 'banoservicio', 'cuartoservicio', 'deposito',
       'estrato', 'estudio', 'garajes', 'gimnasio', 'habitaciones',
       'halldealcobas', 'parqueaderovisitantes', 'piscina', 'piso', 'porteria',
       'remodelado', 'terraza', 'vigilancia', 'zonalavanderia', 'latitud',
       'longitud', 'tiempodeconstruido 16 a 30 años',
       'tiempodeconstruido 9 a 15 años', 'tiempodeconstruido Entre 0 y 5 años',
       'tiempodeconstruido Entre 10 y 20 años',
       'tiempodeconstruido Entre 5 y 10 años',
       'tiempodeconstruido Menos de 1 año',
       'tiempodeconstruido Más de 20 años',
       'tiempodeconstruido Más de 30 años', 'vista Interior',
       'valormetrocuadrado'],
      dtype='object')

Index(['balcon', 'banos', 'banoservicio', 'conjuntocerrado', 'cuartoservicio',
       'deposito', 'estrato', 'estudio', 'garajes', 'gimnasio', 'habitaciones',
       'halldealcobas', 'parqueaderovisitantes', 'piscina', 'piso', 'porteria',
       'remodelado', 'saloncomunal', 'terraza', 'vigilancia', 'zonalavanderia',
       'valoradministracion', 'latitud', 'longitud',
       'tiempodeconstruido 16 a 30 años', 'tiempodeconstruido 9 a 15 años',
       'tiempodeconstruido Entre 10 y 20 años',
       'tiempodeconstruido Más de 20 años', 'valormetrocuadrado'],
      dtype='object')

