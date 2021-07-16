#!/usr/bin/env python
import django
import os
import sys
import requests
import json
from pymysql import connect
import dbinfo

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()
print(BASE_DIR)
#key e31a714730e34d21a2dfcbc8de363774

def insert_multiple(val):
    """Function to insert multiple rows at once"""
    conn = connect(host=dbinfo.myhost, port=3306, user=dbinfo.myuser, password=dbinfo.mypasswd,
                   database=dbinfo.mydatabase,
                   charset="utf8")
    cs = conn.cursor()

    sql = "INSERT INTO realtime_bus_data VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cs.executemany(sql, val)
    conn.commit()

    print(cs.rowcount, "was inserted.")

class Bus:
    def __init__(self):
        self.headers = {
        'Cache-Control': 'no-cache',
        'x-api-key': 'e31a714730e34d21a2dfcbc8de363774',
        }
        self.url = "https://api.nationaltransport.ie/gtfsrtest/?format=json"
    def parse_url(self):
        response = requests.get(self.url, headers=self.headers)
        print(response)
        content = json.loads(response.text)
        self.save_data(content)
    def save_data(self,content):
        """Function that scrapes the GTFS API and makes tuples of the data"""
        conn = connect(host=dbinfo.myhost, port=3306, user=dbinfo.myuser, password=dbinfo.mypasswd,
                       database=dbinfo.mydatabase,
                       charset="utf8")
        cs = conn.cursor()
        cs.execute("TRUNCATE realtime_bus_data")
        conn.commit()

        vals = []
        counter = 0
        #print(content)
        k = len(content["entity"]) - 1
        print(k)
        for i in range(0, k):
            try:
                l = len(content["entity"][i]["trip_update"]["stop_time_update"]) - 1
                value = []
                value.append(str(content["header"]["timestamp"]))
                    #value += ","
                value.append(content["entity"][i]["id"])
                    #value += ","
                value.append(content["entity"][i]["trip_update"]["trip"]["trip_id"])
                    #value += ","
                value.append(content["entity"][i]["trip_update"]["trip"]["start_time"])
                    #value += ","
                value.append(content["entity"][i]["trip_update"]["trip"]["start_date"])
                    #value += ","
                value.append(content["entity"][i]["trip_update"]["trip"]["route_id"])
                    #value += ","
                value.append(str(content["entity"][i]["trip_update"]["stop_time_update"][l]["stop_sequence"]))
                    #value += ","
                try:
                    value.append(content["entity"][i]["trip_update"]["stop_time_update"][l]["arrival"]["delay"])
                except Exception as e:
                    value.append(str(0))
                    #$value += ","
                try:
                    value.append(str(content["entity"][i]["trip_update"]["stop_time_update"][l]["departure"]["delay"]))
                except Exception as e:
                    value.append(str(0))
                    #value += ","
                value.append(content["entity"][i]["trip_update"]["stop_time_update"][l]["stop_id"])
                    #res = tuple(map(value.split(str, ', ')))
                    #value += ","
                tup = tuple(value)
                vals.append(tup)
                counter += 1
            except Exception as e:
                print("error")
                print(e)
                print(value)
                tup = tuple(value)
                vals.append(tup)
                counter += 1
                continue

                #continue
            if counter == k-1:
                #send the remaining rows
                insert_multiple(vals)
                break

            if counter % 999 == 0:
                #send every 999 rows (sql limit)
                insert_multiple(vals)
                vals = []


    def run(self):
        self.parse_url()

b = Bus()
b.parse_url()


