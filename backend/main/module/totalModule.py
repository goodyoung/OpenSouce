import pandas as pd
import requests
from haversine import haversine
import json
import os
import re
# print(os.getcwd())
os.chdir("./main/module") ##경로 설정

## 따릉이 거리 계산
class bike_distance:
    def __init__(self,lat,long):
        print(os.getcwd())
        self.df = pd.read_csv('./datasets/data1.csv')
        self.my_location = (lat,long)
        self.result = self.location_data(self.df,self.my_location)
    def te(self, text):
        pattern = r"\d+\."
        result = re.sub(pattern, "", text)
        result = result.strip()
        return result
    def distance_calc(self, df, my_location):
        bike_location = (df['stationLatitude'], df['stationLongitude'])
        distance = haversine(my_location, bike_location, unit = 'm')
        return distance

    def location_data(self, df,location):
        df[['stationLatitude','stationLongitude']] = df[['stationLatitude','stationLongitude']].astype(float)
        df['distance'] = df[['stationLatitude','stationLongitude']].apply(self.distance_calc, axis =1, my_location = self.my_location)
        df['stationName'] = df['stationName'].apply(self.te)
        distance_index = list(df['distance'].sort_values().index)[:5]
        location_json = json.loads(df.loc[distance_index].to_json(orient = 'records',force_ascii=False))
        return location_json
    
## 주소 -> 위,경도
class ChangeAddress:
    def __init__(self,address):
        self.address = address
        self.result = self.changeAddress(self.address)
        
    def changeAddress(self, address):
        url = f'https://dapi.kakao.com/v2/local/search/address.json?query={address}'
        headers = {"Authorization": "KakaoAK ddade78155e5ff37aab8ddc00f07c0df"} #kakao rest api key 암호화 작업 필요함.
        try:
            address_json = requests.get(url, headers=headers).json()['documents'][0]
            return address_json['x'],address_json['y']
        except:
            return False
    
## 문화재, 공원, 거리 등
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
        for name in ['park','culture','heritage']:  #더 추가할 수 있겠지?
            filename = f'./datasets/Seoul {name}.csv'
            df = pd.read_csv(filename)
            self.dic[name] = self.location_data(df,self.my_location)