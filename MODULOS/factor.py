import numpy as np
import pandas as pd
from sklearn.linear_model import Lasso
from sklearn import linear_model
from sklearn.preprocessing import MinMaxScaler
from geopy import Nominatim
import matplotlib.pyplot as plt
#import geopandas
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import requests as req 
from  bs4 import BeautifulSoup
import os
import itertools
import MODULOS.factor as f
import datetime as dt
import pandas_datareader.data  as web
from functools import reduce
import re
import itertools
import statsmodels.api as sm

def path():
    return os.getcwd() + "\Data"

def call_tin():
    df =  pd.read_html("https://tin.titularizadora.com/valoracion-titulos-y-calculadora-historial/",thousands=".")[0]
    df = df.set_index([df.columns[0]]).pct_change()
    df.dropna(inplace=True)
    df.index = pd.to_datetime(df.index)
    df.index.rename(name="Fecha",inplace=True)
    df.index = pd.to_datetime(df.index,yearfirst=True,format="%Y/%m").to_period("D")
    df.sort_values(by=["Fecha"],axis=0,ascending=True,inplace=True)
    df.columns = ["Tin"]
    df = ((1+df).rolling(window=90).apply(np.prod)-1).dropna()
    return df 

def call_IPVU():
    """
    Link: https://totoro.banrep.gov.co/estadisticas-economicas/faces/pages/charts/line.xhtml?facesRedirect=true
    """
    df = pd.read_csv(path()+ "\IPVU.csv",index_col="Fecha").pct_change().dropna()
    df.index = pd.to_datetime(df.index,yearfirst=True,format="%Y/%m").to_period("D")
    df.columns = ["IPVU"]
    return df

def call_IPVN():
    """
    Indices segun municipios y estratos 
    Link: https://www.dane.gov.co/index.php/estadisticas-por-tema/precios-y-costos/indice-de-precios-de-la-vivienda-nueva-ipvn#:~:text=En%20el%20cuarto%20trimestre%20de,incremento%20de%205%2C79%25.
    """
    IPVN = pd.read_excel(path()+"\IPVN_ind_mpi_estr_IVtrim20_indice.xls",skiprows=range(0,8),usecols="A:K").dropna(axis=0,how="all")
    IPVN = IPVN.iloc[1:-4]
    Y = IPVN["Año"].dropna()
    Y = list(np.repeat(Y,4))
    Y = list(re.findall(r"\d+", str(Y)))
    Q = list(IPVN["Trimestre"])
    q = []
    for i in Q:
        if (i == "I"):
            q.append(str(3))
        if (i == "II"):
            q.append(str(6));
        if i == "III":
            q.append(str(9));
        elif i=="IV" :
            q.append(str(12))
    Date_ind = []
    for i, j in zip(Y, itertools.cycle(q)):
        Date_ind.append(i+"/"+j)
    IPVN = pd.DataFrame(data=np.array(IPVN["Bogotá"]),columns=["IPVN-Bogotá"],index=Date_ind).pct_change().dropna()
    IPVN.index = pd.to_datetime(IPVN.index,yearfirst=True,format="%Y/%m") + pd.tseries.offsets.SemiMonthEnd(2)
    IPVN.index = pd.to_datetime(IPVN.index,yearfirst=True,format="%Y/%m/%d").to_period("D")
    IPVN.index.rename(name="Fecha",inplace=True)
    return IPVN

def cartera_vivienda():
    """
    Link: https://www.superfinanciera.gov.co/inicio/informes-y-cifras/cifras/establecimientos-de-credito/informacion-periodica/mensual/tasa-de-interes-y-desembolsos-por-modalidad-de-credito-60955
    """
    c_vivienda = pd.read_excel(path()+"\carteradevivienda.xlsx",sheet_name="CONSOLIDADO",usecols="A:BO",skiprows=range(0,4))
    data = np.array(c_vivienda.iloc[:-1,-2] + c_vivienda.iloc[:-1,-1])
    ind = c_vivienda.iloc[:-1,0]
    m = [i.split(' DE ', 1)[0] for i in list(ind)]
    mes =[]
    for i in m:
        mes.append(i.lower())
    año = [i.split(' DE ', 1)[1] for i in list(ind)]
    q = []
    for i in mes:
        if (i == "enero"):
            q.append(str(1))
        if (i == "febrero"):
            q.append(str(2));
        if i == "marzo":
            q.append(str(3));
        if (i == "abril"):
            q.append(str(4))
        if (i == "mayo"):
            q.append(str(5));
        if i == "junio":
            q.append(str(6));
        if (i == "julio"):
            q.append(str(7))
        if (i == "agosto"):
            q.append(str(8));
        if i == "septiembre":
            q.append(str(9));
        if (i == "octubre"):
            q.append(str(10))
        if (i == "noviembre"):
            q.append(str(11));
        elif i=="diciembre" :
            q.append(str(12))
    date = ["-".join(i) for i in list(zip(año,q))]
    c_vivienda = pd.DataFrame(data=data,index=date,columns=["Cartera_inmobiliaria"]).pct_change().dropna()
    c_vivienda.index.rename(name="Fecha",inplace=True)
    c_vivienda.index = pd.to_datetime(c_vivienda.index,yearfirst=True,format="%Y/%m") + pd.tseries.offsets.SemiMonthEnd(2)
    c_vivienda.index = pd.to_datetime(c_vivienda.index,yearfirst=True,format="%Y/%m/%d").to_period("D")
    c_vivienda.sort_values(by=["Fecha"],axis=0,ascending=True,inplace=True)
    c_vivienda = ((1+c_vivienda).rolling(window=3).apply(np.prod)-1).dropna()
    return c_vivienda

def tasa():
    file = pd.read_excel(path()+"\carteradevivienda.xlsx", None);
    names = list(file.keys())[1:-1]
    r = re.compile(".*\d")
    name = list(filter(r.match, names)) 
    
    dfs = []
    for n  in name:
        t_vivienda = pd.read_excel(path()+"\carteradevivienda.xlsx",sheet_name=n,usecols="A:AI",skiprows=range(0,5))
        t_vivienda.dropna(axis=0,how="all",inplace=True)
        data = np.array((t_vivienda.iloc[:-1,-1].replace("N.A.",np.nan)).replace(" ",np.nan))
        ind = t_vivienda.iloc[:-1,0]

        m = [i.split(" DE ", 1)[0] for i in list(ind)]
        mes =[]
        for i in m:
            mes.append(i.lower())
        año = [i.split("DE " , 1)[1] for i in list(ind)]
        q = []
        mes = [i.replace(" ", "") for i in list(mes)]
        for i in mes:
            if re.search("en",i) != None:
                q.append(str(1))
            if re.search("fe",i) != None:
                q.append(str(2));
            if re.search("mar",i) != None:
                q.append(str(3));
            if re.search("ab",i) != None:
                q.append(str(4));
            if re.search("may",i) != None:
                q.append(str(5));
            if re.search("jun",i) != None:
                q.append(str(6));
            if re.search("jul",i) != None:
                q.append(str(7));
            if re.search("ag",i) != None:
                q.append(str(8));
            if re.search("se",i) != None:
                q.append(str(9));
            if re.search("oc",i) != None:
                q.append(str(10))
            if re.search("no",i) != None:
                q.append(str(11));
            elif re.search("di",i) != None:
                q.append(str(12))
        date = ["-".join(i) for i in list(zip(año,q))]
        t_vivienda = pd.DataFrame(data=data,index=date,columns=[n]).pct_change().dropna()
        t_vivienda.index.rename(name="Fecha",inplace=True)
        t_vivienda.index = pd.to_datetime(t_vivienda.index,yearfirst=True,format="%Y/%m") + pd.tseries.offsets.SemiMonthEnd(2)
        t_vivienda.index = pd.to_datetime(t_vivienda.index,yearfirst=True,format="%Y/%m/%d").to_period("D")
        t_vivienda.sort_values(by=["Fecha"],axis=0,ascending=True,inplace=True)
        t_vivienda = ((1+t_vivienda).rolling(window=3).apply(np.prod)-1).dropna()
        dfs.append(t_vivienda)
        all_r = reduce(lambda left,right: pd.merge_asof(left,right,left_index=True,right_index=True),dfs)
        r = pd.DataFrame(all_r.sum(axis=1),columns=["% tasas prom"])
        return(r)

def call_inflacion():
    """
    link: https://totoro.banrep.gov.co/estadisticas-economicas/faces/pages/charts/line.xhtml?facesRedirect=true
    """
    inf = pd.read_csv(path() + "\inflacion.csv",parse_dates=True,index_col=["Fecha"])/100
    inf.columns = ["Inflacion"]
    inf.index = pd.to_datetime(inf.index,yearfirst=True,format="%Y/%m").to_period("D")
    return inf

def call_banrep():
    """
    Link: https://totoro.banrep.gov.co/estadisticas-economicas/faces/pages/charts/line.xhtml?facesRedirect=true
    """
    Brep = pd.read_csv(path() + "\\tasa_banrep.csv",parse_dates=True,index_col=["Fecha"])/100
    Brep.columns = ["tasa interv"]
    Brep.index = pd.to_datetime(Brep.index,yearfirst=True,format="%Y/%m").to_period("D")
    return Brep

def call_usd_cop():
    """
    Link: Spot price -Yahoo finance 
    """
    star = dt.datetime(2018,1,1)
    end = dt.datetime(2022,1,11)
    x = pd.DataFrame(web.DataReader("COP=X",'yahoo',star,end)["Close"]).pct_change().dropna()
    x.index.rename(name="Fecha",inplace=True)
    x.index = pd.to_datetime(x.index,yearfirst=True,format="%Y/%m").to_period("D")
    x = ((1+x).rolling(window=90).apply(np.prod)-1).dropna()
    x.columns = ["USD/COP"]
    return x

def call_PIB():
    """
    PIB a precios constantes 
    Link: https://www.dane.gov.co/index.php/estadisticas-por-tema/cuentas-nacionales/cuentas-nacionales-trimestrales/pib-informacion-tecnica
    """  
    PIB= pd.read_excel(path()+"\Anexos_produccion_constantes_IV_2020.xlsx",sheet_name="Cuadro 1", skiprows=range(0,76),usecols="C:BO") 
    # list of rows you want to omit at the beginning  # columns to use 
    PIB.set_index("Unnamed: 2",inplace =True)
    PIB = (PIB.iloc[0:-5,4:]).dropna(axis=0,how="all")
    Y = list(PIB.iloc[0].dropna())
    Y = list(re.findall(r"\d+", str(Y)))
    Y = np.repeat(Y,4)
    Q = list(PIB.iloc[1])
    q = []
    for i in Q:
        if (i == "I"):
            q.append(str(3))
        if (i == "II"):
            q.append(str(6));
        if i == "III":
            q.append(str(9));
        elif i=="IV" :
            q.append(str(12))
    Date_ind = []
    for i, j in zip(Y, itertools.cycle(q)):
        Date_ind.append(i+"/"+j)
    PIB = pd.DataFrame(np.array(PIB.iloc[-1]),index=Date_ind,columns=["PIB"])/100
    PIB.index = pd.to_datetime(PIB.index,yearfirst=True,format="%Y/%m") + pd.tseries.offsets.SemiMonthEnd(2)
    PIB.index = pd.to_datetime(PIB.index,yearfirst=True,format="%Y/%m/%d").to_period("D")
    PIB.index.rename(name="Fecha",inplace=True)
    return PIB

def factor():
    a = f.call_IPVN()
    b = f.call_IPVU()
    c = f.call_tin()
    d = f.cartera_vivienda()
    r = f.tasa()
    e = f.call_inflacion()
    f_ = f.call_banrep()
    g = f.call_usd_cop()
    h = f.call_PIB()

    dfs =[a,b,c,d,r]
    all_d = reduce(lambda left,right: pd.merge_asof(left,right,left_index=True,right_index=True),dfs)

    ew = 1/len(all_d.columns)
    #     n = np.asarray([ew]*len(dfs)).shape[0]
    #     init_guess = np.repeat(1/n, n)

    MM = pd.DataFrame((all_d*ew).sum(axis=1),columns=["M_inmobiliario"])

    d =[e,f_,g,h,MM]
    facm = reduce(lambda left,right: pd.merge_asof(left,right,left_index=True,right_index=True),d)

    facm = facm.dropna()

    lm = sm.OLS(endog=facm.iloc[:,-1].astype(float),exog=(facm.iloc[:,0:4]).astype(float)).fit()
    lm.summary()
    
    return lm.predict((facm.iloc[:,0:4]))[-1]


