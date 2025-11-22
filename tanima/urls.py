# tanima/urls.py

from django.urls import path
from . import views

app_name = 'tanima'
urlpatterns = [
    path('', views.tanima_view, name='anasayfa'),
]