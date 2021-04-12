import requests
from bs4 import BeautifulSoup
import re
import geopandas

url = "https://oaiee.scj.gov.co/agc/rest/services/Tematicos_Pub/CifrasSCJ/MapServer/1"
reqs = requests.get(url)
soup = BeautifulSoup(reqs.text, 'lxml')

a = []
for tag in soup.find_all("li"):
     a.append([tag.text])

d = []
for i in range(len(a)):
    I = re.search("[A-Z0-9]+" ,a[i][0]).group()
    N = re.sub("\r","",re.search(r'alias: (.*)', a[i][0]).group(1)) 
    d.append([[I],[N]])

crimen = geopandas.read_file(path_0+"/Data/DAIUPZ.geojson")

nem = [d[i][0][0] for i in range(0,len(d))]
names = [d[i][1][0] for i in range(0,len(d))]
replacements = dict(zip(nem, names))

cols = []
for i in range(0,len(d)):
    txt =  crimen.columns.to_list()[i]
    r = re.sub('({})'.format('|'.join(map(re.escape, replacements.keys()))), lambda m: replacements[m.group()], txt)
    cols.append(r)

crimen.columns = cols + [crimen.columns[-1]]

############## ejecutar crimen y filtrar y extraer los puntos de la zona del crimen

total = [col for col in crimen.columns if 'Total ' and "2020" in col][0:-5]
total = total+ [crimen.columns[-1]]

crimen = crimen[total]

############## Punto central de cada upz 
lat = crimen["geometry"].centroid.y
lon = crimen["geometry"].centroid.x
crimen = crimen.iloc[:,:-1]
crimen["lat"] = lat
crimen["lon"] = lon
crimen.to_csv(path_0+"\\Data\\df_crimenupz.csv")