from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import UserManager

class MyUser(AbstractBaseUser):
    id = models.AutoField(primary_key=True, auto_created=True)
    name = models.TextField(default="", max_length=50)
    email = models.EmailField(
        verbose_name='Email Address', max_length=70, unique=True,)
    is_active = models.BooleanField(default=True)
    admin = models.BooleanField(default=False)
    password = models.TextField()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_name(self):
        return self.name

    def __str__(self):
        return self.email



class favourite_place(models.Model):
    place_name = models.CharField(max_length=50)
    latitude = models.FloatField()
    longitude = models.FloatField()
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.name + ": " + self.place_name