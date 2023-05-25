from django.urls import path
from . import views
app_name = 'main'

urlpatterns = [
    path('', views.SearchView.as_view()),
    path('map/', views.MapView.as_view(),name='map'),
    path('map/bike_coordinate/', views.bike_coordinate, name='total_json'),
    
    # path('map/many_coordinate/', views.many_coordinate, name='total_json2'),
]