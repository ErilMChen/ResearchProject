from django.db import models

# Create your models here.
class StopTimesGoogle(models.Model):
    id = models.AutoField(primary_key=True)
    trip_id = models.CharField(max_length=45, blank=True, null=True)
    arr_time = models.CharField(max_length=45, blank=True, null=True)
    dep_time = models.CharField(max_length=45, blank=True, null=True)
    stop_id = models.CharField(max_length=45, blank=True, null=True)
    stopp_seq = models.CharField(max_length=45, blank=True, null=True)
    stop_headsign = models.CharField(max_length=45, blank=True, null=True)
    pickup_type = models.CharField(max_length=45, blank=True, null=True)
    drop_off_type = models.CharField(max_length=45, blank=True, null=True)
    shape_dist_traveled = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stop_times_google'