import googlemaps
from datetime import datetime
import math

class Location:
    
    def __init__(self):
        self.googlemaps = googlemaps.Client(key='AIzaSyBhF6x7vBJdK_8EQ0kqp_Hyb8wcwhWedDQ')


    def get_location(self, add_):
        self.add = add_
        self.info = self.googlemaps.geocode(self.add)
        
        if self.info != []:
            
            self.latitude = self.info[0]['geometry']['location']['lat']
            self.longitude = self.info[0]['geometry']['location']['lng']
            
        else:
            self.latitude = 0.0
            self.longitude = 0.0


class Calculator_coor:

    def __init__(self, lat_1, lon_1, lat_2, lon_2):
        
        self.lat_1 = lat_1
        self.lon_1 = lon_1
        self.lat_2 = lat_2
        self.lon_2 = lon_2
    
    
    def get_dist(self):
        
        rad = math.pi / 180
        
        dlat = self.lat_2 - self.lat_1
        dlon = self.lon_2 -self.lon_1
        
        R=6372.795477598
        
        a = (math.sin(rad*dlat/2))**2 + math.cos(rad*self.lat_1)*math.cos(rad*self.lat_2)*(math.sin(rad*dlon/2))**2
        
        distancia = 2 * R * math.asin(math.sqrt(a))
        
        self.dist = distancia 
        

class Score:
    
    def __init__(self, lat_, lon_, df_ss, n_):
        
        self.lat_ = lat_
        self.lon_ = lon_
        self.df_ss = df_ss
        self.n_ = n_
                
    def get_score(self):
        
        self.df_ss['dist_rel'] = 0.0
        
        for ff in range(0, self.df_ss.shape[0]):
            
            dist_ = Calculator_coor(self.lat_, self.lon_, self.df_ss.iloc[ff, 0], self.df_ss.iloc[ff, 1])
            dist_.get_dist()
            
            self.df_ss.iloc[ff, - 1] = dist_.dist
            
        self.df_ss.sort_values(by = ['dist_rel'], ascending = True, inplace = True)   
        
        self.sum_n = self.df_ss['dist_rel'][:self.n_].sum()
        self.mean_n = self.df_ss['dist_rel'][:self.n_].mean()
        


class Prima_df:
    
    def __init__(self, lat_, lon_, df, dist_):
        
        self.lat_ = lat_
        self.lon_ = lon_
        self.df = df
        self.dist_ = dist_
                
    def get_score(self):
        
        self.df['dist_rel'] = 0.0
        
        for ff in range(0, self.df.shape[0]):
            
            dist_ = Calculator_coor(self.lat_, self.lon_, self.df.iloc[ff, 0], self.df.iloc[ff, 1])
            dist_.get_dist()
            
            self.df.iloc[ff, - 1] = dist_.dist
            
        self.df.sort_values(by = ['dist_rel'], ascending = True, inplace = True)   
        self.df = self.df[self.df['dist_rel'] < self.dist_]
        
        
        

class Prima_dis_desvest:
    
    def __init__(self, lat_, lon_, df, n_):
        
        self.lat_ = lat_
        self.lon_ = lon_
        self.df = df
        self.n_ = n_
                
    def get_score(self):
        
        self.df_ss['dist_rel'] = 0.0
        
        for ff in range(0, self.df_ss.shape[0]):
            
            dist_ = Calculator_coor(self.lat_, self.lon_, self.df_ss.iloc[ff, 0], self.df_ss.iloc[ff, 1])
            dist_.get_dist()
            
            self.df_ss.iloc[ff, - 1] = dist_.dist
            
        self.df_ss.sort_values(by = ['dist_rel'], ascending = True, inplace = True)   
        
        self.sum_n = self.df_ss['dist_rel'][:self.n_].sum()
        self.mean_n = self.df_ss['dist_rel'][:self.n_].mean()

