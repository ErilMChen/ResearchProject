import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

##This is just a test file

from users.models import my_stations, MyUser

user = MyUser.objects.filter(email='hello@hello.com').get()
print(type(user))

#user2 = MyUser(email='hihi@email.com', password='dublinbus')
#user2.save()
user2 = MyUser.objects.filter(email='hihi@email.com').get()

station_id = '6'
current_user = user2
station_id = '8240DB000231'
user_fav = my_stations(stop_id = station_id, user = current_user)
user_fav.check_num()
user_fav.save()