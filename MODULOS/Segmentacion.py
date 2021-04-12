import numpy as np
import pandas as pd
import os
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from geopy import Nominatim

class Seg_train:
    
    def __init__(self, df):
        
        self.df = df

    def get_segmetacion(self, valor_vemta_max = 930000000,
                        valor_vemta_min = 185000000):
        
        self.valor_vemta_max = valor_vemta_max
        self.valor_vemta_min = valor_vemta_min
    
        df_train = self.df
        df_train_seg1 = df_train[(df_train['area'] > 104) & (df_train['area'] < 230) & 
                                     (df_train["estrato"]>=2) & (df_train["estrato"]<=5) &
                                     (df_train["tipoinmueble"] != "Apartamento") &
                                     (df_train["valorventa"] > self.valor_vemta_min) & (df_train["valorventa"] <= self.valor_vemta_max) &
                                     (df_train["saloncomunal"].isna()) &
                                     (df_train["conjuntocerrado"]==0) & 
                                     ((df_train["valoradministracion"] == 0) | (df_train["valoradministracion"].isna())) &
                                     (df_train["banos"]>=2) & (df_train["banos"]<=4) & 
                                     (df_train["ascensor"].isna()) &
                                     ((df_train["piso"].isna()) | (df_train["piso"] <=4)) &
                                     (df_train["tiponegocio"] == "Venta") &
                                     (df_train["tiempodeconstruido"] != "Remodelado")].copy()
        
        df_train_seg1.drop(labels=["tipoinmueble","tiponegocio"],axis=1,inplace=True)
        df_train_seg1 = pd.get_dummies(df_train_seg1,drop_first=True,prefix_sep=" ")
        df_train_seg1.fillna(0,inplace=True)
        df_train_seg1.set_index(keys=["id"],inplace=True,verify_integrity=True)
        
        '''
        print("area", df_train_seg1["area"].min(),"-",df_train_seg1["area"].max())
        print("estrato",df_train_seg1["estrato"].min(),"-",df_train_seg1["estrato"].max())
        print("valor venta", df_train_seg1["valorventa"].min(),"-",df_train_seg1["valorventa"].max())
        print(df_train_seg1["saloncomunal"].value_counts())
        print(df_train_seg1["conjuntocerrado"].value_counts())
        print("baños",df_train_seg1["banos"].min(),"-",df_train_seg1["banos"].max())
        print("ascensor",df_train_seg1["ascensor"].value_counts())
        print("Piso",df_train_seg1["piso"].min(),df_train_seg1["piso"].max())
        print("mxn",df_train_seg1.shape)
        '''

        locator = Nominatim(user_agent="myGeocoder")
        # location = locator.geocode(input("Punto de referencia")) ### terminal del norte
        location = locator.geocode("terminal del norte")
        l_1 =  location.longitude, location.latitude
        print("Latitude = {}, Longitude = {}".format(location.latitude, location.longitude))
        
        locator = Nominatim(user_agent="myGeocoder")
        # location = locator.geocode(input("Punto de referencia")) ## suba bilbao
        location = locator.geocode("suba bilbao")
        l_2 =  location.longitude, location.latitude
        print("Latitude = {}, Longitude = {}".format(location.latitude, location.longitude))
        
        locator = Nominatim(user_agent="myGeocoder")
        # location = locator.geocode(input("Punto de referencia")) ### fontibon recodo
        location = locator.geocode("fontibon recodo") 
        l_3 =  location.longitude, location.latitude
        print("Latitude = {}, Longitude = {}".format(location.latitude, location.longitude))
        
        locator = Nominatim(user_agent="myGeocoder")
        # location = locator.geocode(input("Punto de referencia")) ### cai san josé bosa
        location = locator.geocode("cai san josé bosa")
        l_4 =  location.longitude, location.latitude
        print("Latitude = {}, Longitude = {}".format(location.latitude, location.longitude))
        
        locator = Nominatim(user_agent="myGeocoder")
        # location = locator.geocode(input("Punto de referencia")) ### los molinos del sur
        location = locator.geocode("los molinos del sur")
        l_5 =  location.longitude, location.latitude
        print("Latitude = {}, Longitude = {}".format(location.latitude, location.longitude))
        
        locator = Nominatim(user_agent="myGeocoder")
        # location = locator.geocode(input("Punto de referencia")) ### vitelma
        location = locator.geocode("vitelma") 
        l_6 =  location.longitude, location.latitude
        print("Latitude = {}, Longitude = {}".format(location.latitude, location.longitude))
        
        locator = Nominatim(user_agent="myGeocoder")
        # location = locator.geocode(input("Punto de referencia")) ### fundacion cardioinfantil
        location = locator.geocode("fundacion cardioinfantil")
        l_7 =  location.longitude, location.latitude
        print("Latitude = {}, Longitude = {}".format(location.latitude, location.longitude))
        
        coordinates = [l_1,l_2,l_3,l_4,l_5,l_6,l_7]
        
        data_Q = list(range(0,(df_train_seg1.shape[0])))
        
        in_perimeter = []
        
        for i in data_Q:
            point = Point(df_train_seg1["longitud"].iloc[i],df_train_seg1["latitud"].iloc[i])
            polygon = Polygon(coordinates)
            a = polygon.contains(point)
            in_perimeter.append(a)
            
        in_perimeter = pd.DataFrame(in_perimeter,columns=["in perimeter"],index=[df_train_seg1.index])
        
        df_train_seg1 =pd.merge(left=df_train_seg1,right=in_perimeter,how="inner",on="id")
        
        df_train_seg1 = df_train_seg1[(df_train_seg1["in perimeter"] == True)]
        df_train_seg1.drop(labels=["in perimeter"],axis=1,inplace=True)
        #### Verificar como filtar tiempo de construido 16 -30 y 10 20 años
        
        df_train_seg1 = df_train_seg1.loc[:,(df_train_seg1 != 0).any(axis=0)]
        df_train_seg1["valormetrocuadrado"] = df_train_seg1["valorventa"]/df_train_seg1["area"]
        df_train_seg1 = df_train_seg1.drop(labels=["area","valorventa"],axis=1)
                
        self.df_train_0 = df_train_seg1

    
#class Seg_test:


class Seg_test:
    
    def __init__(self, df, columas_df):
        
        self.df = df
        self.columas_df = columas_df

    def get_segmetacion(self):

        df_test_seg1 = self.df
        #df_test_seg1 = tabla_1 
        
        df_test_seg1.drop(labels=["tipoinmueble","tiponegocio"],axis=1,inplace=True)
        df_test_seg1 = pd.get_dummies(df_test_seg1,drop_first=True,prefix_sep=" ")
        df_test_seg1.fillna(0,inplace=True)
        df_test_seg1.set_index(keys=["id"],inplace=True,verify_integrity=True)
        
        df_test_seg1["valormetrocuadrado"] = df_test_seg1["valorventa"]/df_test_seg1["area"]
        df_test_seg1 = df_test_seg1.drop(labels=["area","valorventa"],axis=1)
        
        df_test_seg1 = df_test_seg1.reindex(self.columas_df, axis = 1)
        df_test_seg1.fillna(0, inplace = True)

        self.df_test_0 = df_test_seg1

