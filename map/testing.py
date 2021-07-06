

import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()
from users.models import my_stations, MyUser
from pymysql import connect
from favourites import dbinfo
import datetime
import json

#joe=MyUser(email='joe@joe.com', password='hello11111')
stations = my_stations.objects.filter().values('stop_id').distinct()
print(stations)