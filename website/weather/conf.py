"""
Used to wrap up Weather App specific settings
"""
import os

from django.conf import settings
from appconf import AppConf

class WeatherConf(AppConf):
    API_KEY = os.environ['WEATHER_API_KEY'] if 'WEATHER_API_KEY' in os.environ else None

    class Meta:
        prefix = 'weather'