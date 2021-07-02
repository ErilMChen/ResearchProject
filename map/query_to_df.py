import mysql.connector
import dbinfo
import json
from sqlalchemy import create_engine
import os
import pandas as pd
import django
os.environ.setdefault('DJANGO_SETTING_MODULE', 'MyDjango.settings')
django.setup()
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
import map.models as m
import sqlite3

mydb = mysql.connector.connect(
            host=dbinfo.myhost,
            user=dbinfo.myuser,
            passwd=dbinfo.mypasswd,
            database=dbinfo.mydatabase,
            charset=dbinfo.mycharset
        )

from datetime import date
import calendar
my_date = date.today()
day = calendar.day_name[my_date.weekday()].lower()

engine = create_engine(dbinfo.engine)
row_query = """SELECT t1.* FROM dubbusdb.final_merged_routes as t1
            right join day_""" + day + """_routes as t2
            on t1.routeID = t2.routeID
            order by bus_lineID, direction;"""

df1 = pd.read_sql_query(row_query, engine)
df1.to_json(orient="table", index=False)

m.RoutesDayModels.objects.all().delete()

df1.to_sql('routes_day_models', engine, if_exists='replace')