from django.shortcuts import render, redirect
from django.views import View
from .module.totalModule import bike_distance, ChangeAddress, Distance
from django.http import JsonResponse
import json
import os
from pathlib import Path
from django.contrib.auth.models import User
from .models import History
#api
def bike_coordinate(request):
        with open('datasets/json_data_2.json', 'r') as f:
            data = json.load(f)
        return JsonResponse(data)
    
# main view
class SearchView(View):
    template_name = 'main/search.html'
    def get(self, request):  
        #아무 기능 없음 일단 만듬
        bo = request.user.is_authenticated
        if bo:
            print('로그인 성공?')
            # request.session['user_id'] = request.user.username
        else:
            print('불가')
        
        ## 검색 기록이니까 db에 업데이트를 하여서
        return render(request, self.template_name)
        

class MapView(View):
    template_name = "main/map.html"

    # def get(self, request,context):
    #     print('연결 성공 ㅎㅎ')
    #     print(context)
    #     return render(request, self.template_name)

    def post(self,request):
        # 유저 로그인 상태일 때 True
        bo = request.user.is_authenticated
        # 사용자 검색 기록 저장
        if bo:
            db_user = User.objects.get(username = request.user.username) # filter | get 방식
            h = History(user=db_user, search_history=request.POST['location'])
            h.save()
        else:
            pass
        ret  = {}
        address = str(request.POST['location'])
        reu = ChangeAddress(address)
        # if reu == False: #False일 때 하는 alter처리하는 로직을 짜자...... ㅎㅎ
        lat = float(reu.result[1])
        long = float(reu.result[0])
        my_location_data = [str(address),lat,long]    
        ret['address'] = json.dumps(my_location_data,ensure_ascii=False)
        #따릉이 및 다른 건물들 거리 게산
        a,b = bike_distance(lat,long), Distance(lat,long)
        bike = a.result
        building = b.dic
        building['bike'] = bike
        
        context = building
        
        for name in ["bike","culture","heritage","park"]:
            temp = []
            for i in context[name]:
                i = dict(i.items())
                dum = json.dumps(i,ensure_ascii=False)
                temp.append(dum)
            ret[name] = temp
            
        return  render(request, self.template_name, context = ret) 
    
    





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