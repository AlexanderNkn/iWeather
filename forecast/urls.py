from django.urls import path
from . import views


urlpatterns = [
    path('', views.CityView.as_view(), name='city'),
    path('fore/', views.fore, name='add_comment'),
]