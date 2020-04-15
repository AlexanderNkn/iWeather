import requests
from django.http import HttpResponse
from django.shortcuts import render
from .models import CityForm


def get_weather(request):
    form = CityForm(request.POST or None)
    url = 'http://api.openweathermap.org/data/2.5/weather?q=Москва&APPID=31e0c786808dd5e6d6a9d72af60d24d4'
    if form.is_valid():
        count = 0
        try:
            response = requests.get(url)
            count += 1
        except requests.ConnectionError as e:
            return HttpResponse(f'<сетевая ошибка - {e}>')
        if response.status_code == 200:
            return render(request, 'index.html', {'response': response.json, 'form': form})
        else:
            return HttpResponse(f'<ошибка на сервере погоды, код {response.status_code}>')
    else:
        form = CityForm(request.POST or None)
        return render(request, 'index.html', {'form': form})
