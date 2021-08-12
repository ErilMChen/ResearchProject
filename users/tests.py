from django.test import TestCase
import unittest
import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()
from users.models import MyUser, my_stations
from django.test import Client



#Unit testing users

class MyUserTest(unittest.TestCase):
    def test_create(self):
        #clear the object from database before testing
        usertest = MyUser.objects.filter(email='test@test.com')
        if usertest.exists():
            MyUser.objects.filter(email='test@test.com').delete()
        count = MyUser.objects.count()
        user = MyUser(email='test@test.com', password='dublinbus', name= 'MrTest')
        user.save()
        post = MyUser.objects.count()
        self.assertEqual(count +1, post)

    def test_fields(self):
        usertest = MyUser.objects.filter(email='test@test.com').values()
        email = usertest[0]['email']
        name = usertest[0]['name']
        ## password can be tested in this case as it has not been hashed by the forms.py file
        password = usertest[0]['password']
        self.assertEqual(email, 'test@test.com')
        self.assertEqual(name, 'MrTest')
        self.assertEqual(password, 'dublinbus')



class Test_Stations(unittest.TestCase):
    def test_add_stations(self):
        count = my_stations.objects.filter(stop_id='1234567').count()
        usertest = MyUser.objects.filter(email='test@test.com').first()
        stop_test = '1234567'
        ob = my_stations(stop_id=stop_test, user=usertest)
        ob.save()
        count2 = my_stations.objects.filter(stop_id=stop_test).count()
        self.assertEqual(count+1, count2)

    def test_addition_limit(self):
        usertest = MyUser.objects.filter(email='test@test.com').first()
        count = my_stations.objects.filter(user=usertest).count()
        #print(count)
        ## now try to add more than 5 stations
        for i in range(0,10):
            ob = my_stations(stop_id=i, user=usertest)
            ob.check_num()
            ob.save()
        count2 = my_stations.objects.filter(user=usertest).count()
        #print(count2)
        ## attempted to add 10 but will only keep 5 at a time
        self.assertTrue(count2 < 6)

    def log_in_test(self):
        # testing user login post form
        #this test will fail if the password is changed
        usertest = MyUser.objects.filter(email='test@test.com')
        if usertest.exists():
            MyUser.objects.filter(email='test@test.com').delete()
        c = Client()
        user = MyUser(email='test@test.com', password='dublinbus', name='MrTest')
        logged_in = c.post('login/', {'username': 'test@test.com', 'password': 'dublinbus'})
        self.assertTrue(logged_in)

    def users_registration_post_test(self):
        #testing user creation post form
        usertest = MyUser.objects.filter(email='test1@test.com')
        if usertest.exists():
            MyUser.objects.filter(email='test1@test.com').delete()
        c = Client()
        creation = c.post('users/', {'username': 'test1@test.com', 'password1': 'dublinbus'})
        usertest = MyUser.objects.filter(email='test1@test.com')
        if usertest.exists():
            count = MyUser.objects.filter(email='test1@test.com').count()
            print(count)
        self.assertTrue(count = 1)




if __name__ == '__main__':
    unittest.main()