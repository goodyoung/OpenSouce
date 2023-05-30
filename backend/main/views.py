from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView
from .module.totalModule import bike_distance, ChangeAddress, Distance
from django.http import JsonResponse
import json
from django.contrib.auth.models import User
from .models import History
from django.contrib import messages

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
            print('여기는 오면 안된다.')
            db_user = User.objects.get(username = request.user.username) # filter | get 방식
            h = History(user=db_user, search_history=request.POST['location'])
            h.save()
        else:
            print('여기는 와줘라')
            pass
        ret  = {}
        address = str(request.POST['location'])
        reu = ChangeAddress(address)
        
        # 주소가 정확하지 않을 때
        try:
            lat = float(reu.result[1])
            long = float(reu.result[0])
            print(lat,long)
        except:
            messages.warning(request, "주소가 정확하지 않습니다. 다시 입력해주세요.")
            return redirect('main:search')
        
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
    
class Mypage(ListView):
    template_name ='main/search_history.html' # 디폴트 템플릿명: <app_label>/<model_name>_list.html
    context_object_name = 'object_list' # 디폴트 컨텍스트 변수명 :  object_list
    def get_queryset(self): # 컨텍스트 오버라이딩
        bo = self.request.user.is_authenticated
        if bo:
            db_user = User.objects.get(username = self.request.user.username) # filter | get 방식
            print('dbdbdbdb',db_user)
            return History.objects.order_by('created_at')
        else:
            messages.warning(self.request, "로그인이 필요한 서비스 입니다. 로그인을 해주시길 바랍니다.")
            print('여긴 안오니이이??')
            
            return redirect('common:login')#render(self.request,'main/search.html')#redirect('main:search')
        # print(History.objects.order_by('created_at'))
        





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