import os
import django
import sys
## required to run paramaters in main package. If does not run in pycharm,
## add to 'DJANGO_SETTING_MODULE', 'MyDjango.settings' in Edit Configurations
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTING_MODULE', 'mysite.settings')
django.setup()
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

import json
import requests
import time
from datetime import datetime
import weather.models


def collect_weather(lati, longi):
    '''This function gathers current weather data'''

    URL = "https://api.openweathermap.org/data/2.5/onecall?lat=" + str(lati) + "&lon=" + str(
        longi) + "&exclude=minutely&appid=c0df90e98d85453f86f46197e2a4c551"

    response = requests.get(URL)
    weather_obj = json.loads(response.text)
    weather_info = ()
    try:
        long = weather_obj['lon']
        lat = weather_obj['lat']
        today = weather_obj['current']
        date1 = today['dt']
        ts = str(datetime.fromtimestamp(date1))
        temp = today['temp']
        feels_like = today['feels_like']
        pressure = today['pressure']
        humidity = today['humidity']
        uvi = today['uvi']
        wind_speed = today['wind_speed']
        clouds = today['clouds']
        visibility = today['visibility']
        weather_detail = today['weather']
        for i in weather_detail:
            for value in i:
                if value == 'main':
                    main = i[value]
                elif value == 'description':
                    desc = i[value]

        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        time_added = time.time()

        # clear all table data
        weather.models.currentWeather.objects.all().delete()

        mod = weather.models.currentWeather(timestamp=ts,
         time=current_time, longitude=long, latitude=lat, uvi=uvi, 
         feels_like=feels_like, pressure=pressure, humidity=humidity, 
         wind_speed=wind_speed, cloudy=clouds, mainweather=main, time_added=time_added)
        mod.save()

    except Exception as e:
        print(e)

collect_weather(53, 6)

