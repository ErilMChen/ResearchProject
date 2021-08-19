from datetime import datetime
import pytz
country_time_zone = pytz.timezone('Europe/Dublin')
country_time = datetime.now(country_time_zone)
print(country_time.strftime("Date is %d-%m-%y and time is %H:%M:%S"))

import pytz
country_time_zone = pytz.timezone('Europe/Dublin')
country_time = datetime.now(country_time_zone)
now = country_time.strftime("%H:%M:%S")
nowh = int(now[0:2])
nowm = now[3:5]
print(nowh, nowm)
