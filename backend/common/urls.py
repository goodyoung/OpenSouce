from django.urls import path
from django.contrib.auth import views as auth_views

app_name = 'common'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='common/login.html'), name='login'),
    #register path도 추가해야함 template_name='common/register.html'
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]