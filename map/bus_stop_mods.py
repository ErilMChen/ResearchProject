import os
import django
## required to run paramaters in main package. If does not run in pycharm,
## add to 'DJANGO_SETTING_MODULE', 'MyDjango.settings' in Edit Configurations

os.environ.setdefault('DJANGO_SETTING_MODULE', 'MyDjango.settings')
django.setup()
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

import map.models as m


# SHOWING NUMBER OF BUS ROUTE OBJECTS WE HAVE -- this is the all_bus_routes table in the database
#They are now linked. There are 30000 objects - the route rows

my_total = m.MapAllroutedata.objects.count()

my_total = m.RoutesDayModels.objects.count()



print(my_total)