import requests
import json
from pymysql import connect
import dbinfo

#key e31a714730e34d21a2dfcbc8de363774

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
        conn = connect(host=dbinfo.myhost, port=3306, user=dbinfo.myuser, password=dbinfo.mypasswd, database=dbinfo.mydatabase,
                            charset="utf8")
        cs = conn.cursor()
        print(content)
        k = len(content["entity"]) - 1
        print(k)
        cs.execute("TRUNCATE realtime_bus_data")
        for i in range(0, k):
            try:
                print(i)
                l = len(content["entity"][i]["trip_update"]["stop_time_update"]) - 1
                value = "insert into realtime_bus_data values("
                value += str(content["header"]["timestamp"])
                value += ","
                value += "\"" + str(content["entity"][i]["id"]) + "\""
                value += ","
                value += "\"" + str(content["entity"][i]["trip_update"]["trip"]["trip_id"]) + "\""
                value += ","
                value += "\"" + str(content["entity"][i]["trip_update"]["trip"]["start_time"]) + "\""
                value += ","
                value += "\"" + str(content["entity"][i]["trip_update"]["trip"]["start_date"]) + "\""
                value += ","
                value += "\"" + str(content["entity"][i]["trip_update"]["trip"]["route_id"]) + "\""
                value += ","
                value += str(content["entity"][i]["trip_update"]["stop_time_update"][l]["stop_sequence"])
                value += ","
                try:
                    value += str(content["entity"][i]["trip_update"]["stop_time_update"][l]["arrival"]["delay"])
                except Exception as e:
                    value += str(0)
                value += ","
                try:
                    value += str(content["entity"][i]["trip_update"]["stop_time_update"][l]["departure"]["delay"])
                except Exception as e:
                    value += str(0)
                value += ","
                value += "\"" + str(content["entity"][i]["trip_update"]["stop_time_update"][l]["stop_id"]) + "\""
                value += ");"
                print(value)
            except Exception as e:
                print("error")
                print(value)
            cs.execute(value)
            conn.commit()
            continue
        cs.close()
        conn.close()

    def run(self):
        self.parse_url()

b = Bus()
b.parse_url()