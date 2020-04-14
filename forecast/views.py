import requests
from django.http import HttpResponse


def index(request):
    url = f'http://wttr.in/Khimki'
    weather_parameters = {
        'format': 2,
        'M': ''
    }
    try:
        response = requests.get(url, params=weather_parameters)
    except requests.ConnectionError:
        return HttpResponse('<сетевая ошибка>')
    if response.status_code == 200:
        return HttpResponse(response)
    else:
        return HttpResponse('<ошибка на сервере погоды>')
