#!/usr/bin/env python
import os
import json
import django
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()

with open(os.path.abspath('static/paths.json')) as config_file:
    config = json.load(config_file)

def collect_weather_forecast():
    #forecastScrape.collect_weather_forecast(53.3, 6.2)
    os.system(config['python_path'] + ' ' + config['forecast_weather_file'])

def collect_current_weather():
    #current_weather_scraper.collect_weather(53.3, 6.2)
    os.system(config['python_path'] + ' ' + config['current_weather_file'])

def collect_road_report():
    #current_weather_scraper.collect_weather(53.3, 6.2)
    os.system(config['python_path'] + ' ' + config['road_report'])

#collect_current_weather()
#collect_weather_forecast()
#collect_road_report()
