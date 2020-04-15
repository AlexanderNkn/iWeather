import os

import requests
from django.http import HttpResponse
from django.shortcuts import render
from dotenv import load_dotenv

from .models import CityForm

load_dotenv()
APPID = os.getenv('APPID')

def get_weather(request):
    city = request.POST.get('city','')
    form = CityForm(request.POST or None)
    url = 'http://api.openweathermap.org/data/2.5/weather'
    params = {
        'q': city,
        'APPID': APPID,
        'lang': 'ru',
        'units': 'metric'
    }
    if form.is_valid():
        try:
            response = requests.get(url, params,)
        except requests.ConnectionError as e:
            return HttpResponse(f'<сетевая ошибка - {e}>')
        if response.status_code == 200:
#            return HttpResponse(response)
            return render(request, 'index.html', {'response': response.json, 'form': form})
        else:
            return HttpResponse(f'<ошибка на сервере погоды, код {response.status_code}>')
    else:
        form = CityForm(request.POST or None)
        return render(request, 'index.html', {'form': form})
