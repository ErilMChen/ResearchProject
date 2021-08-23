import django
import os
import requests
from itertools import chain
import re
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()
from favourites.models import StopTimesGoogle
from pymysql import connect
import datetime
import json
from mysite import dbinfo
from map.models import NameToID
#now = str(datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f%Z")
#now = str(datetime.datetime.now(datetime.timezone.utc).strftime("%H:%M:%S"))
from datetime import datetime
import pytz
country_time_zone = pytz.timezone('Europe/Dublin')
country_time = datetime.now(country_time_zone)
now = country_time.strftime("%H:%M:%S")
nowh = int(now[0:2])
nowm = now[3:5]
from datetime import datetime

#changes

def difference(h1, m1, h2, m2):
    """This gets time difference between now and the time in the schedule to see if it is within the
    next hour"""
    h2 = int(h2)

    t1 = int(h1) * 60 + int(m1)
    t2 = int(h2) * 60 + int(m2)
    #print(t2-t1)
    if 0 < t1-t2 and t1-t2 <60:
        return True
    else:
        return False



def get_times(stop_ids):
    """This function checks the rows of the schedule and creates an array of the rows in the next hour.
    It also calls the real time API data function and checks which rows need to be changed"""
    data = []
    url = 'https://www.timeapi.io/api/Time/current/zone?timeZone=Europe/Dublin'
    response = requests.get(url)
    res = json.loads(response.text)
    nowh = res['hour']
    nowm = res['minute']
    for stop_id in stop_ids:
        there_are_buses = False
    #get updates for this stop
        API_updates = get_API(stop_id)
        #filter the stop time objects for this stop
        sched1 = StopTimesGoogle.objects.filter(stop_id=stop_id, arr_time__regex=r'^(?:(?:'+ str(nowh) + ':)?([0-5]?\d):)?([0-5]?\d)$').values()
        sched2 = StopTimesGoogle.objects.filter(stop_id=stop_id, arr_time__regex=r'^(?:(?:' + str(
            nowh + 1) + ':)?([0-5]?\d):)?([0-5]?\d)$').values()
        sched = list(chain(sched1, sched2))
        # if it doesnt exist in our schedule
        if not sched:
            default = {'id': None, 'trip_id': '0000-0000', 'arr_time': 'Stop Not Available in Transport Ireland Bus Times', 'dep_time': 'N/A', 'stop_id': stop_id, 'stopp_seq': 'N/A',
                   'stop_headsign': ' N/A', 'pickup_type': 'N/A',
                   'drop_off_type': 'N/A', 'shape_dist_traveled': 'N/A', 'stop_name': str(stop_id)}
            data.append(default)
            continue
        for row2 in sched:
            #check if the trip in the row runs today (see check_day function)
            if check_day(row2['trip_id']) == True:
                try:
                    # get the time from the row
                    h = row2['arr_time'][0:2]
                    m = row2['arr_time'][3:5]
                    # check if within he next hour
                    if difference(h, m, nowh, nowm) == True:
                        there_are_buses = True
                        print(there_are_buses)
                        # check if API updated need to be applied
                        for i in range(0, len(API_updates)):
                            if row2['trip_id'] == API_updates[i][0]:
                                print('match')
                                new_times = calculate_new_time(row2, API_updates[i])
                                print(new_times[0], 'new time index 1')
                                print('old row', row2)
                                row2['arr_time'] = new_times[0]
                                row2['dep_time'] = new_times[1]
                                # data.append(row2)
                                # continue
                        # get the name of the stop and append to the row
                        name = NameToID.objects.values('stop_name', 'stop_id').filter(
                            stop_id=row2['stop_id']).distinct()
                        data1 = list(name)
                        stop_name = data1[0]['stop_name']
                        # print(stop_name)
                        row2['stop_name'] = stop_name
                        data.append(row2)
                        # print(row2)
                except Exception as e:
                    print(e)

            else:
                continue

        if there_are_buses == False:
                # if theres no buses in this time, send empty dic
            name = NameToID.objects.values('stop_name', 'stop_id').filter(stop_id=row2['stop_id']).distinct()
            data1 = list(name)
            stop_name = data1[0]['stop_name']
            no_bus = {'id': None, 'trip_id': '0000 - 0000', 'arr_time': 'No buses scheduled',
                          'dep_time': 'N/A', 'stop_id': stop_id, 'stopp_seq': 'N/A',
                          'stop_headsign': ' N/A', 'pickup_type': 'N/A',
                          'drop_off_type': 'N/A', 'shape_dist_traveled': 'N/A', 'stop_name': stop_name}
            data.append(no_bus)
            continue



    if len(data) == 0:
        #if theres no data
        return return_json(data, 'no buses')

    # if there is data
    return return_json(data, 'parse')

def return_json(data, command):
    if command == 'no buses':
        list = [{"Route": 'None', "Bus": 'N/A', "Stop": 'No Buses Scheduled For Your Stops', "Seq": 'none'}]

    else:
        #split the rows into dic
        list = [{"Route": x['trip_id'], "Bus": x['trip_id'].split("-")[1], "Arrival Time": x['arr_time'],
                 "Departure Time": x['dep_time'], "Stop": x['stop_id'], "Sequence": x['stopp_seq'], 'Name': x['stop_name'].split(",")[0]} for x in data]
    for i in range(0,len(list)):
        print(list[i])
    return json.dumps(list)

def get_API(stop_id):
    """This functioon checks the live API data for a given stop and returns an array of the needed data"""
    conn = connect(host=dbinfo.myhost, port=3306, user=dbinfo.myuser, password=dbinfo.mypasswd,
                   database=dbinfo.mydatabase,
                   charset="utf8")
    cs = conn.cursor()
    cs.execute("SELECT * from realtime_bus_data where stop_id = %s", stop_id)
    myresult = cs.fetchall()
    res = []
    for i in range(0, len(myresult)):
        res1 = []
        trip = str(myresult[i][2])
        route_id = myresult[i][5]
        stop_seq = myresult[i][6]
        arrival_delay = myresult[i][7]
        dep_delay = myresult[i][8]
        res1 += trip, route_id, stop_seq, arrival_delay, dep_delay
        res.append(res1)
    return res


def calculate_new_time(schedule, delays):
    """This function alters the scheduled times according to the API updates"""
    from datetime import timedelta as dt
    scheduled_arr = schedule['arr_time']
    scheduled_dep = schedule['dep_time']
    arr_delay = int(delays[3])
    dep_delay = int(delays[4])
    print(scheduled_arr, arr_delay)

    #code adapted from https://stackoverflow.com/questions/10663720/how-to-convert-a-time-string-to-seconds
    time1 = scheduled_arr
    time2 = scheduled_dep
    print(time2, time1)
    #chnage to seconds
    s1 = sum(x * int(t) for x, t in zip([3600, 60, 1], time1.split(":")))
    s2 = sum(x * int(t) for x, t in zip([3600, 60, 1], time2.split(":")))
    new_arr = s1 + int(arr_delay)
    new_dep = s2 + int(arr_delay)
    new_arr = str(dt(seconds=new_arr))
    new_dep = str(dt(seconds=new_dep))

    return new_arr, new_dep


import datetime as dd
def check_day(route):
    """This function checks if the route in the row is allowed today"""
    row_route = route.split(".")[1]
    routes = []
    today = str(dd.datetime.now().today().weekday())
    available = {
        "y1001" : ['6'],
        "y1002" : ['4'],
        "y1003" : ["0", "1", "2", "3", "4"],
         "y1004" : ["0", "6"],
        "y1005" : ["2", "3", "4"],
        "y1006" : ["5"],
        'y1009' : ['0', "1", "2", "3", "4", '5','6']
    }
    for key, value in available.items():
        for day in value:
            if today == day:
                routes.append(key)

    if row_route in routes:
        return True
    else:
        return False
