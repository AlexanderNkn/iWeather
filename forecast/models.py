from django.db import models
from django.forms import ModelForm


PERIOD_CHOICES = (
    ('H', 'Почасовой прогноз'),
    ('D', 'Прогноз на неделю'),
    ('W', 'Двухнедельный прогноз'),
)

class City(models.Model):
    '''Модель описывает город и период прогноза погоды'''
    city = models.CharField(max_length=200, verbose_name='')
    period = models.CharField(max_length=1, choices=PERIOD_CHOICES,)

    def __str__(self):
        return self.city


class CityForm(ModelForm):
    class Meta:
        model = City
        fields = ['city',] # 'period']