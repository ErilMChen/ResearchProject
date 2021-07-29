from django.db import models
# Create your models here.

class currentWeather(models.Model):
    timestamp = models.TextField()
    time = models.TextField()
    longitude = models.FloatField()
    latitude = models.CharField(max_length = 45)
    uvi = models.TextField(max_length=50)
    feels_like = models.TextField(max_length=50)
    pressure = models.TextField(max_length=50)
    humidity = models.TextField(max_length=50)
    wind_speed = models.TextField(max_length=50)
    cloudy = models.TextField(max_length=50)
    mainweather = models.TextField(max_length=50)
    time_added = models.CharField(max_length = 45)

class Forecast(models.Model):
    id = models.IntegerField
    fdate = models.TextField()
    temp = models.TextField()
    temp_max = models.TextField()
    temp_min = models.TextField()
    feelslike = models.TextField()
    pressure = models.FloatField()
    humidity = models.CharField(max_length=45)
    main = models.TextField(max_length=50)
    wind_speed = models.TextField(max_length=50)
    wind_deg = models.TextField()
    desc = models.TextField()

class AA_Road_Report(models.Model):
    lat = models.FloatField()
    long = models.FloatField()
    location = models.TextField()
    report = models.TextField()