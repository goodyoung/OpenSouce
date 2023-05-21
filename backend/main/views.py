from django.shortcuts import render, redirect, reverse
from django.views import View
from .module.totalModule import bike_distance, ChangeAddress, Distance
class SearchView(View):
    template_name ='main/search.html'
    def get(self, request):        
        return render(request, self.template_name)
        
    def post(self,request):
        ## input값 받아오는 작업만 하면 된다.
        address = '서울 중구 회현동1가'
        #주소 -> 위경도 변환
        reu = ChangeAddress(address)
        lat = float(reu.result[1])
        long = float(reu.result[0])        
        #따릉이 및 다른 건물들 거리 게산
        a,b = bike_distance(lat,long), Distance(lat,long)
        bike = a.result
        building = b.dic

        return redirect('main:map')
    
class MapView(View):
    template_name = "main/map.html"

    def get(self, request):
        print('연결 성공 ㅎㅎ')
        return render(request, self.template_name)
    
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