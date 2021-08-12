import os
import django
import json
import unittest
import datetime
import time
from users.models import MyUser
from django.test import Client
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()
import get_sched2 as schedule_return
now = str(datetime.datetime.now().time())
nowh = int(now[0:2]) + 1
nowm = now[3:5]



#UNIT TESTING for the return of the schedule script. More detailed tests are in the users directory

from users.models import MyUser, my_stations

class TestSchedule(unittest.TestCase):
    ret = schedule_return.get_times('testing')
    data = json.loads(ret)

    def test_call(self):
        #check it returns a string object to be parsed
        self.assertTrue(type(self.ret) == str)

    def test_non_existing(self):
        #test for a stop that does not exist
        #returns an array (loaded above) with 7 fields saying does not exist
        field_count = 0
        route = self.data[0]['Route']
        bus = self.data[0]['Bus']
        arr = self.data[0]['Arrival Time']
        dep = self.data[0]['Departure Time']
        seq = self.data[0]['Sequence']
        for i in range(0, len(self.data)):
            ## our data has 7 chosen fields
            field_count += 1
        self.assertTrue(route == '0000-0000')
        self.assertTrue(bus == '0000')
        self.assertTrue(arr == 'Stop Not Available in Transport Ireland Bus Times')
        self.assertTrue(dep == 'N/A')
        self.assertTrue(seq == 'N/A')
        self.assertTrue(field_count == 7)

    def test_existing(self):
        ## this is time dependant
        # testing the return for an existing stop - checking name, time within the hour, and stop num
        ret = schedule_return.get_times(['8220DB004432'])
        self.data1 = json.loads(ret)
        fields = []
        #print(self.data1)
        stop = self.data1[0]['Stop']
        bus = self.data1[0]['Bus']
        arr = self.data1[0]['Arrival Time']
        #check time less than 60 mins from now
        h = arr.split(':')[0]
        m = h = arr.split(':')[1]
        t1 = int(h) * 60 + int(m)
        t2 = int(nowh) * 60 + int(nowm)
        diff = t2-t1
        dep = self.data1[0]['Departure Time']
        seq = self.data1[0]['Sequence']
        name = self.data1[0]['Name']

        self.assertTrue(stop=='8220DB004432')
        self.assertTrue(diff < 60)
        self.assertTrue(name == 'Griffith Downs')

if __name__ == '__main__':
    unittest.main()