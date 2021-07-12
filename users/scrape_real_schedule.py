import csv
import mysql
from pymysql import connect
import dbinfo
x = ('1625124748', '1164.y1003.60-77A-b12-1.161.I', '1164.y1003.60-77A-b12-1.161.I', '07:30:00', '20210701', '60-77A-b12-1', '64', '120', '120', '8220DB000340')


match = '60-33E-b12-1'
match2 = '8220DB000351'
import datetime
now = str(datetime.datetime.now().time())
nowh = now[0:2]
nowm = now[3:5]






## WE NEED TO DELETE THIS FILE





import csv
from datetime import datetime

def difference(h1, m1, h2, m2):
    if h1 >= h2:
        if h1 == h2:
            if m1 >= m2:
                # convert into minutes
                t1 = int(h1) * 60 + int(m1)
                t2 = int(h2) * 60 + int(m2)

                if (t1 == t2):
                    return False
                else:
                    #get difference
                    diff = t2 - t1
                    h = (int(diff / 60)) % 24

    # calculating minutes from difference
                m = diff % 60
                return True

            else:
                return False
    else:
        return False



def get_times(stop_id):
    API_updates = get_API(stop_id)
    print('UPDATES', API_updates)
    with open('stop_times.csv', 'rt') as f2:
        reader2 = csv.reader(f2, delimiter=',')
        next(reader2)
        for row2 in reader2:
            expected_delays = False
            if stop_id == str(row2[3]):
                try:
                    t = datetime.strptime(row2[1], '%H:%M:%S').time()
                    t = row2[1]
                    h = row2[1][0:2]
                    m = row2[1][3:5]
                    if difference(h, m, nowh, nowm) == True:
                        for i in range(0, len(API_updates)):
                            if row2[0] == API_updates[i][0]:
                                expected_delays = True
                                new_times = calculate_new_time(row2, API_updates[i])
                                print(new_times)
                        print(row2)
                except Exception as e:
                    if int(row2[1][0:2]) >= 24:
                        row2[1] = "0" + str(int(row2[1][0:2]) - 24) + row2[1][2:]
                        (datetime.strptime(row2[1], '%H:%M:%S'))
                        #print(row2[1])
                        t = datetime.strptime(row2[1], '%H:%M:%S').time()
                        t = row2[1]
                        h = row2[1][0:2]
                        m = row2[1][3:5]
                        if difference(h, m, nowh, nowm) == True:
                            print(row2)


#get_times('8510B5550801')


def get_API(stop_id):
    conn = connect(host=dbinfo.myhost, port=3306, user=dbinfo.myuser, password=dbinfo.mypasswd,
                   database=dbinfo.mydatabase,
                   charset="utf8")
    cs = conn.cursor()
    cs.execute("SELECT * from realtime_bus_data where stop_id = %s", stop_id)
    myresult = cs.fetchall()
    print(len(myresult))
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
    from datetime import timedelta as dt
    scheduled_arr = schedule[1]
    scheduled_dep = schedule[2]
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

get_times('8220DB006115')
