from django.db import models

# Create your models here.
class BusStops(models.Model):
    stoppointid = models.IntegerField()
    stop_name = models.CharField(max_length = 45)
    stop_lat = models.FloatField()
    stop_long = models.FloatField()
    direction = models.IntegerField()
    routes_serving = models.TextField()

class NameToID(models.Model):
    stop_id = models.CharField(max_length = 45)
    stop_name = models.CharField(max_length = 45)
    stop_lat = models.FloatField()
    stop_long = models.FloatField()
    stop_num = models.IntegerField()