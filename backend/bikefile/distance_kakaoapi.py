import requests
import numpy as np
import pandas as pd

def elec_location(region,page_num):
    url = 'https://dapi.kakao.com/v2/local/search/keyword.json'
    params = {'query': region,'page': page_num}
    headers = {"Authorization": #kakaoapi}
    places = requests.get(url, params=params, headers=headers).json()['documents']
    return places

def elec_info(places):
    X = []
    Y = []
    for place in places:
        X.append(float(place['x']))
        Y.append(float(place['y']))
    ar = np.array([X, Y]).T
    df = pd.DataFrame(ar, columns = ['X', 'Y'])
    return df

def keywords(location_name):
    df = None
    local_name = elec_location(location_name, 1)
    local_elec_info = elec_info(local_name)
    df = local_elec_info
    df = pd.concat([df, local_elec_info],join='outer', ignore_index = True)       
    return df

def make_map(dfs):
    latitude_sum = 0
    longitude_sum = 0
    for i in range(len(dfs)):
        latitude_sum+=float(dfs['Y'][i])
        longitude_sum+=float(dfs['X'][i])
    a = latitude_sum/len(dfs['Y'])
    b = longitude_sum/len(dfs['X'])
    return a,b
