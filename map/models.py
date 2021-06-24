from django.db import models

# Create your models here.
class BikeStation(models.Model):
    bk_id = models.IntegerField(primary_key=True, null = False)
    bk_contract_name = models.CharField(max_length = 45)
    bk_name = models.CharField(max_length = 45)
    bk_address = models.CharField(max_length = 45)
    bk_lat = models.FloatField()
    bk_lng = models.FloatField()
    bk_banking = models.CharField(max_length = 45)
    bk_bouns = models.CharField(max_length = 45)
    bk_bike_stands = models.IntegerField()
    bk_available_bike_stands = models.IntegerField()
    bk_available_bikes = models.IntegerField()
    bk_status = models.CharField(max_length = 45)
    bk_last_update = models.CharField(max_length = 45)

class RoutesDayModels(models.Model):
    routeid = models.CharField(db_column='routeID', max_length=45, blank=True, null=True)  # Field name made lowercase.
    progrnum = models.FloatField(blank=True, null=True)
    bus_lineid = models.CharField(db_column='bus_lineID', max_length=45, blank=True, null=True)  # Field name made lowercase.
    stoppointid = models.CharField(db_column='stoppointID', max_length=22, blank=True, null=True)  # Field name made lowercase.
    direction = models.CharField(max_length=45, blank=True, null=True)
    stop_name = models.CharField(max_length=45, blank=True, null=True)
    stop_long = models.CharField(max_length=45, blank=True, null=True)
    stop_lat = models.CharField(max_length=45, blank=True, null=True)
    stop_id = models.CharField(max_length=45, blank=True, null=True)
    year = models.CharField(max_length=45, blank=True, null=True)
    id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'dubbusdb.routes_day_models'