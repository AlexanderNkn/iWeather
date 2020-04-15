import requests
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import CreateView
from .models import CityForm


def fore(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q=Москва&APPID=31e0c786808dd5e6d6a9d72af60d24d4'
    
    try:
        response = requests.get(url)
    except requests.ConnectionError:
        return HttpResponse('<сетевая ошибка>')
    if response.status_code == 200:
        return render(request, 'index.html', {'response': response.json})
    else:
        return HttpResponse('<ошибка на сервере погоды>')

class CityView(CreateView):
    form_class =  CityForm
    success_url = "forecast" # куда переадресовать пользователя после успешной отправки формы
    template_name = "index.html"
