import os
import json
import folium
import requests
import pandas as pd
import chromedriver_autoinstaller

from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from haversine import haversine
from folium.plugins import MiniMap
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


# 따릉이 대여소 api
def create_api():
    data = []
    for i in range(3):
        url = f'http://openapi.seoul.go.kr:8088/704e68517730363134317958547662/json/bikeList/{i}001/{i+1}000'
        req = requests.get(url).json()
        for s in req['rentBikeStatus']['row']:
            temp = []
            for j in list(s.keys()):
                temp.append(s[j])
            data.append(temp)   
    df = pd.DataFrame(data, columns=list(req['rentBikeStatus']['row'][0].keys()))
    return df

# 거리 계산
def latilong(df, my_location):
    dat = []
    data_set = []
    for ty in range(len(df)):
        dat.append((df['stationLatitude'].iloc[ty],df['stationLongitude'].iloc[ty]))
        
    for rt in dat:
        sc = (float(rt[0]),float(rt[1]))
        data_set.append(haversine(my_location, sc, unit = 'm'))
    df_ty = pd.DataFrame(data_set, columns = ['distance'])
    return df_ty

# 최적의 따릉이 대여소
def bestdistance(df_ty,s):
    distance_list = list(df_ty['distance'].sort_values()[:3].index)
    df_total = s.loc[distance_list,['rackTotCnt','stationName','parkingBikeTotCnt','shared','stationLatitude','stationLongitude']].reset_index()
    df_total = pd.merge(df_total, df_ty['distance'].sort_values()[:3].reset_index(), on='index')
    return df_total




# 최적의 따릉이 대여소 시각화 
def make_map2(df_total_distance):
    Latitude = df_total_distance['stationLatitude'].astype(float).mean()
    Longitude = df_total_distance['stationLongitude'].astype(float).mean()
    m = folium.Map(location=[Latitude,Longitude], zoom_start=12)
    minimap = MiniMap() 
    m.add_child(minimap)
    data = []
    for i,j in zip(df_total_distance['stationLatitude'], df_total_distance['stationLongitude']):
        li = []
        li.append(i)
        li.append(j)
        data.append(li)
    for mark in data:
        folium.Marker(mark).add_to(m)
    m.save('아쌍.html')
    return True

# 따릉이 사진 캡쳐
def picture():
    chrome_options = webdriver.ChromeOptions()  
    chrome_options.add_argument("--headless") 
    file_name = 'my_screenshot.png'
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    #오류시: 파일 경로 수정
    browser.get("C:/Users/goyangi/jupyter-work/wowow//Crawling/따릉이/따릉이 최종/아쌍.html")
    button = browser.find_element(By.CSS_SELECTOR, ".leaflet-control-zoom-in")
    for i in range(3) :
        button.click()
        sleep(1)
    browser.save_screenshot(file_name)
    browser.close()

    path = os.getcwd()
    tot_path = path+'\\'+file_name
    tot_path = tot_path.replace('\\','/')
    return tot_path