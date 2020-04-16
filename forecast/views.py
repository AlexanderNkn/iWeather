import os

import requests
from django.http import HttpResponse
from django.shortcuts import render
from dotenv import load_dotenv

from .models import CityForm, SKY_CHOICES, WEAR_CHOICES


load_dotenv()
APPID = os.getenv('APPID')

def get_weather(request):
    '''Получает информацию с сервера погоды'''
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
            response = requests.get(url, params)
        except requests.ConnectionError as e:
            return HttpResponse(f'<сетевая ошибка - {e}>')
        if response.status_code == 451:
            return HttpResponse('<Превышено количество обращений к серверу погоды. Перезагрузите страницу.>')
        if response.status_code == 200:
            weather = response.json()
            wear = get_wear(weather)
            return render(request, 'index.html', {'weather': weather, 'form': form, 'wear': wear})
        else:
            return HttpResponse(f'<ошибка на сервере погоды, код {response.status_code}>')
    else:
        form = CityForm(request.POST or None)
        return render(request, 'index.html', {'form': form})


def get_wear(weather):
    '''Составляет рекомендации что одеть, в зависимости от погоды'''
    try:
        id = weather.get('weather')[0].get('id')
        sky = weather.get('weather')[0].get('main')
        temp = weather.get('main').get('temp')
        if id in [800, 801]:
            msg2 = SKY_CHOICES.get('S')
        elif id not in [503, 504] and sky in ['Rain', 'Drizzle']:
            msg2 = SKY_CHOICES.get('R')
        elif id in [503, 504] and sky == 'Thunderstorm':
            msg2 = SKY_CHOICES.get('HR')
        else:
            msg2 = ''
        if temp < 5:
            msg1 = WEAR_CHOICES.get('Cold')
        elif temp < 20:
            msg1 = WEAR_CHOICES.get('Light')
        elif temp < 30:
            msg1 = WEAR_CHOICES.get('Comf')
        else:
            msg1 = WEAR_CHOICES.get('Hot')
        msg = f'{msg1} и {msg2}' if msg2 else f'{msg1}.'
        return msg
    except Exception:
        return 'Сервер погоды зажал необходимую информацию. Придумайте, что одеть, сами.'
