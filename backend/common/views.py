from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from common.forms import UserForm

def register(request):
    if request.method == "POST":
        print(request.POST)
        form = UserForm(request.POST)
        if form.is_valid():
            print('11111111111')
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=raw_password)  # 사용자 인증
            # login(request, user)  # 로그인 시키는 거
            return redirect('common:login')
        print('222222222222')
    else:
        print('3333333333333')
        form = UserForm()
    return render(request, 'common/register.html', {'form': form})
    #  return render(
    #      request,
    #      'common/register.html',
    #  )


# def signup(request):
#     if request.method == "POST":
#         form = UserForm(request.POST)
#         if form.is_valid():
#             print('asdaasfasfasfas')
#             form.save()
#             username = form.cleaned_data.get('username')
#             raw_password = form.cleaned_data.get('password1')
#             user = authenticate(username=username, password=raw_password)  # 사용자 인증
#             # login(request, user)  # 로그인 시키는 거
#             return redirect('common:login')
#         print('222232323')
#     else:
#         print('????')
#         form = UserForm()
#     return render(request, 'common/register.html', {'form': form})
 # Create your views here.