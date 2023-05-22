from django.shortcuts import render, redirect
from django.views import View
from .module.totalModule import bike_distance, ChangeAddress, Distance
from django.http import JsonResponse
import json
import os
from pathlib import Path
def bike_coordinate(request):
        with open('datasets/json_data_2.json', 'r') as f:
            data = json.load(f)
        return JsonResponse(data)
# def many_coordinate(request, address):
        # print(address)
        # address = '서울 중구 회현동1가'
        # reu = ChangeAddress(address)
        # # if reu == False: #False일 때 하는 alter처리하는 로직을 짜자...... ㅎㅎ
        # lat = float(reu.result[1])
        # long = float(reu.result[0])
        # print(f'사용자 input은 {address}이고 위 경도는 {(lat,long)}입니다.') 
        # #따릉이 및 다른 건물들 거리 게산
        # a,b = bike_distance(lat,long), Distance(lat,long)
        # bike = a.result
        # building = b.dic
        
        # building['bike'] = bike    
        # return JsonResponse(building)
# /Users/goodyoung/Desktop/GIt/OpenSouce/backend/static/main/data/json_data_2.json
class SearchView(View):
    template_name ='main/search.html'
    def get(self, request):        
        return render(request, self.template_name)
        

    
class MapView(View):
    template_name = "main/map.html"

    # def get(self, request,context):
    #     print('연결 성공 ㅎㅎ')
    #     print(context)
    #     return render(request, self.template_name)
    def post(self,request):
        
        address = '서울 중구 회현동1가'
        reu = ChangeAddress(address)
        # if reu == False: #False일 때 하는 alter처리하는 로직을 짜자...... ㅎㅎ
        lat = float(reu.result[1])
        long = float(reu.result[0])
        print(f'사용자 input은 {address}이고 위 경도는 {(lat,long)}입니다.') 
        #따릉이 및 다른 건물들 거리 게산
        a,b = bike_distance(lat,long), Distance(lat,long)
        bike = a.result
        building = b.dic
        
        building['bike'] = bike
        context = building
        ret  = {}

        for name in ["bike","culture","heritage","park"]:
            for i in context[name]:
                # for key,value in i.items():
                #     i[key] = str(value)
                i = dict(i.items())
                ret[name] = (json.dumps(i,ensure_ascii=False))
        print('ret')

        return  render(request, self.template_name, context = ret) #redirect('main:map', context)
    
    
    # def post(self,request):




## 기존 코드
# def index(request):
#     print(123)
#     return render(
#         request,
#         'main/search.html',
#     )
# def map(request):
#     return render(
#         request,
#         'main/map.html',
#     )