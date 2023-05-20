from django.shortcuts import render

def index(request):
    return render(
        request,
        'main/search.html',
    )
def map(request):
    return render(
        request,
        'main/map.html',
    )
# Create your views here.