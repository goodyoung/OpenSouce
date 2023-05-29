from django.urls import path
from . import views
app_name = 'main'

urlpatterns = [
    path('', views.SearchView.as_view(),name = 'search'),
    path('map/', views.MapView.as_view(),name='map'),
    path('map/bike_coordinate/', views.bike_coordinate, name='total_json'),
    path('mypage/', views.Mypage.as_view(), name='mypage'),
]