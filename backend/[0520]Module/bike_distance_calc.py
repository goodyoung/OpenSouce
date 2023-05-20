import pandas as pd
import requests
from haversine import haversine
import json
# df = pd.read_csv('data1.csv')
# my_location = (37.55564880,126.91062927)

class bike_distance:
    def __init__(self,lat,long):
        self.df = pd.read_csv('data1.csv')
        self.my_location = (lat,long)
        self.result = self.location_data(self.df,self.my_location)
        
    def distance_calc(self, df, my_location):
        bike_location = (df['stationLatitude'], df['stationLongitude'])
        distance = haversine(my_location, bike_location, unit = 'm')
        return distance

    def location_data(self, df,location):
        df[['stationLatitude','stationLongitude']] = df[['stationLatitude','stationLongitude']].astype(float)
        df['distance'] = df[['stationLatitude','stationLongitude']].apply(self.distance_calc, axis =1, my_location = self.my_location)
        distance_index = list(df['distance'].sort_values().index)[:5]
        location_json = json.loads(df.loc[distance_index].to_json(orient = 'records',force_ascii=False))
        return location_json


    