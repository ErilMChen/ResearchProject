#!/usr/bin/python

import datetime
print(datetime.datetime.now())

import datetime

now = str(datetime.datetime.now(datetime.timezone.utc).strftime("%H:%M:%S"))
print(now)

nowh = int(now[0:2]) + 1
nowm = now[3:5]

print(nowh)
print(nowm)
from datetime import datetime, timedelta
from pytz import timezone
import pytz
utc = pytz.utc
eastern = timezone('US/Eastern')
eastern.zone
amsterdam = timezone('Europe/Dublin')
print(amsterdam)
fmt = '%Y-%m-%d %H:%M:%S %Z%z'
loc_dt = eastern.localize(datetime(2002, 10, 27, 6, 0, 0))
print(loc_dt.strftime(fmt))
#2002-10-27 06:00:00 EST-0500
ams_dt = loc_dt.astimezone(amsterdam)
ams_dt.strftime(fmt)
print(ams_dt)

