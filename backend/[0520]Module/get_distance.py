import pandas as pd
import requests
from haversine import haversine
import json

class Distance:
    def __init__(self,lat,long):
        self.my_location = (lat,long)
        self.dic = {}
        self.total()
        
    def distance_calc(self,df, my_location):
        location = (df['latitude'], df['longtitude'])
        distance = haversine(my_location, location, unit = 'm')
        return distance

    def location_data(self,df,location):
        df[['latitude','longtitude']] = df[['latitude','longtitude']].astype(float)
        df['distance'] = df[['latitude','longtitude']].apply(self.distance_calc, axis =1, my_location = self.my_location)
        distance_index = list(df['distance'].sort_values().index)[:5]
        location_json = json.loads(df.loc[distance_index].to_json(orient = 'records',force_ascii=False))
        return location_json   
    
    def total(self):
        for name in ['공원','문화공간','문화재']:  #더 추가할 수 있겠지?
            filename = f'서울 {name}.csv'
            df = pd.read_csv(filename)
            self.dic[name] = self.location_data(df,self.my_location)