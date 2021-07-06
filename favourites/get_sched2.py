import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()
from favourites.models import StopTimesGoogle
from pymysql import connect
from favourites import dbinfo
import datetime
import json
now = str(datetime.datetime.now().time())
nowh = now[0:2]
nowm = now[3:5]
from datetime import datetime

def difference(h1, m1, h2, m2):
    h1 =int(h1)
    h2 = int(h2)+1
    if h1 >= h2:
        if h1 == h2:
            if m1 >= m2:
                # convert into minutes
                t1 = int(h1) * 60 + int(m1)
                t2 = int(h2) * 60 + int(m2)
                if (t1 == t2):
                    return False
                else:
                    return True
    if int(h2) + 1  == int(h1):
        return True
    else:
        return False



def get_times(stop_id):
    #get updates for this stop
    data = []
    API_updates = get_API(stop_id)
    #print('UPDATES', API_updates)
    #filter the stop time objects for this stop
    sched = StopTimesGoogle.objects.filter(stop_id=stop_id).values()
    for row2 in sched:
        if check_day(row2['trip_id']) == True:
            try:
                #get the time from the row
                h = row2['arr_time'][0:2]
                m = row2['arr_time'][3:5]
                #check if within he next hour
                if difference(h, m, nowh, nowm) == True:
                    #check if API updated need to be applied
                    for i in range(0, len(API_updates)):
                        if row2['trip_id'] == API_updates[i][0]:
                            print('match')
                            new_times = calculate_new_time(row2, API_updates[i])
                            print(new_times[0], 'new time index 1')
                            print('old row', row2)
                            row2['arr_time'] = new_times[0]
                            row2['dep_time'] = new_times[1]
                            data.append(row2)
                    data.append(row2)

                    #If the time goes past midnight eg (24:05)
            except Exception as e:
                print(e)
        else:
            continue

    return return_json(data)


#get_times('8510B5550801')

def return_json(data):
    list = [{"route": x['trip_id'], "bus": x['trip_id'].split("-")[1], "arr_time": x['arr_time'], "dep_time": x['dep_time'], "stop": x['stop_id'], "seq": x['stopp_seq']} for x in data]
    #print(json.dumps(list))
    return json.dumps(list)

def get_API(stop_id):

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
        "y1003" : ["0", "1", "2", "3", "4"],
         "y1004" : ["0", "6"],
        "y1005" : ["2", "3", "4"],
        "y1006" : ["5"]
    }
    for key, value in available.items():
        for day in value:
            if today == day:
                routes.append(key)

    if row_route in routes:
        return True
    else:
        return False

get_times('8220B1354201')