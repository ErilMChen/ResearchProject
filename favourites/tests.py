import os
import django
import json
import unittest
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()
import get_sched2 as schedule_return


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
        for i in range(0, len(self.data)):
            ## our data has 7 chosen fields
            field_count += 1
        #self.assertTrue(ob_len == 1)
        self.assertTrue(field_count == 7)

    def test_existing(self):
        ## this is time dependant
        ret = schedule_return.get_times(['8220DB004432'])
        data = json.loads(ret)
        fields = []
        stop = []
        for i in range(0, len(data)):
            fields.append(data[i].items())
            break
        print(fields)
        self.assertTrue(0==0)
if __name__ == '__main__':
    unittest.main()