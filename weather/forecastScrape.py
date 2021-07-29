#!/usr/bin/env python
import os
import django
import sys
## required to run paramaters in main package. If does not run in pycharm,
## add to 'DJANGO_SETTING_MODULE', 'MyDjango.settings' in Edit Configurations
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

import json
import requests
import time
from datetime import datetime
import weather.models as m

def collect_weather_forecast():
    '''function that takes long at lat as parameters and gathers future weather data'''

    URL = "https://api.openweathermap.org/data/2.5/forecast?lat=53.3&lon=6.2&cnt=96&units=metric&appid=c0df90e98d85453f86f46197e2a4c551"

    response = requests.get(URL)
    obj = json.loads(response.text)

    try:
        m.Forecast.objects.all().delete()
        for j in range(0, 38):
            per_day = obj['list'][j]
            ft_date = per_day['dt']
            main = per_day['main']
            dt = per_day['dt_txt']
            weather = per_day['weather']
            desc = weather[0]['description']
            clouds = per_day['clouds']
            winds = per_day['wind']
            timestamp = datetime.fromtimestamp(ft_date)
            timestamp = timestamp.strftime('%d-%m-%Y %H:%M:%S')

            # varibales
            ft_temp = main['temp']
            ft_feels_like = main['feels_like']
            temp_min = main['temp_min']
            temp_max = main['temp_max']
            ft_pressure = main['pressure']
            ft_humidity = main['humidity']
            ft_clouds = clouds['all']
            ft_main = weather[0]['main']
            ft_wind_speed = winds['speed']
            ft_wind_deg = winds['deg']

            #clear all table data

            # make new objects
            forecast = m.Forecast(
                fdate=dt,
                desc= desc,
                humidity= ft_humidity,
                main= ft_main,
                wind_speed = ft_wind_speed,
                pressure= ft_pressure,
                feelslike = ft_feels_like,
                temp=ft_temp,
                temp_max = temp_max,
                temp_min = temp_min,
                wind_deg= ft_wind_deg)
            forecast.save()

            print(ft_temp, ft_feels_like, temp_max, temp_min, ft_pressure, ft_humidity, ft_clouds, ft_main, ft_wind_speed, ft_wind_deg, desc)

    except Exception as e:
        print(e)
        print('error')

    print('done')

collect_weather_forecast()