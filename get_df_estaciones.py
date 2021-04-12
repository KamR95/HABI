import geopandas
import os

path_0 = os.getcwd()

estaciones = geopandas.read_file("https://opendata.arcgis.com/datasets/5365d814bbdd4062a59234eea7d70db7_1.geojson")
estaciones  = estaciones[["nombre_estacion","latitud_estacion","longitud_estacion"]]
estaciones.to_excel(path_0 +"/Data/estaciones.xlsx")