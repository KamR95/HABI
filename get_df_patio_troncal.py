import geopandas
import os

path_0 = os.getcwd()

patio_troncal = geopandas.read_file("https://opendata.arcgis.com/datasets/e98dd255268c474697e5aab94f4ee58a_0.geojson")
patio_troncal = patio_troncal[["nombre_patio_troncal","latitud_patio_troncal","longitud_patio_troncal"]]
patio_troncal.to_excel(path_0 +"/Data/patio_troncal.xlsx")