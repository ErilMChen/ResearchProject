import os
import django
## required to run paramaters in main package. If does not run in pycharm,
## add to 'DJANGO_SETTING_MODULE', 'MyDjango.settings' in Edit Configurations

os.environ.setdefault('DJANGO_SETTING_MODULE', 'MyDjango.settings')
django.setup()
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

import weather.models as m
import xmltodict
import requests
import json


def get_road_incidents():
    URL = "https://www.theaa.ie/api/IncidentService.svc/GetIncidents"
    response = requests.get(URL)
    xmltxt = response.content

    x = xmltodict.parse(xmltxt)
    data_dict = json.dumps(x)

    road_obj = json.loads(data_dict)
    places = road_obj['Places']['Place']
    extract(places)


def extract(obj):
    m.AA_Road_Report.objects.all().delete()

    for i in range(0, len(obj)):
        if obj[i]['Area'] == 'Dublin':
            lati = obj[i]['Lat']
            longi = obj[i]['Long']
            loc = obj[i]['Location']
            reported = obj[i]['Report']


            road_report = m.AA_Road_Report(
                lat= lati,
                long = longi,
                location = loc,
                report = reported
            )

            road_report.save()


get_road_incidents()
