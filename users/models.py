from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models import Count

class MyUserManger(BaseUserManager):
    """This is a custom manager class to create super users/admins. This manages the
    MyUser class"""
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('Email Required!')
        if not username:
            raise ValueError('Username required!')

        user = self.model(
            email = email,
            username = username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")

        user = self.model(
            email=self.normalize_email(email)
        )
        user.set_password(password)
        user.is_admin = True
        user.is_staff = True
        user.is_active = True
        user.save(using=self._db)
        return user

class MyUser(AbstractBaseUser):
    """User class which is set as our django user"""
    id = models.AutoField(primary_key=True, auto_created=True)
    name = models.TextField(default="", max_length=50)
    email = models.EmailField(verbose_name='Email Address', max_length=70, unique=True,)
    is_active = models.BooleanField(default=True)
    admin = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    #password = models.TextField()
    last_login = models.DateTimeField(verbose_name='last_login', auto_now=True)

    objects = MyUserManger()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    #This class does not have extra permissions unless is admin
    def has_module_perms(self, perm, obj=None):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return self.is_admin

class my_plans(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    plan_name = models.CharField(max_length=50)
    start_stop = models.CharField(max_length=50)
    end_stop = models.CharField(max_length=50)
    date = models.CharField(max_length=50)
    time = models.CharField(max_length=50)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    start_lat = models.FloatField(max_length=50)
    start_long = models.FloatField(max_length=50)
    end_lat = models.FloatField(max_length=50)
    end_long = models.FloatField(max_length=50)

    def __str__(self):
        return self.user.name + ": " + self.start_stop + self.end_stop + self.time

    def check_num_plans(self):
        id = self.user.id
        '''This function does not allow the user to have more than 5 plans saved.
        It deletes by the process of last in first out'''
        val = my_plans.objects.filter(user=self.user).count()
        if val > 5:
            all_is = my_plans.objects.filter(user_id=id).values_list('id', flat=True)[1:4]
            print(all_ids)
            my_plans.objects.filter(user_id=id).exclude(pk__in=list(all_ids)).delete()


class my_stations(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    stop_id = models.TextField()
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)

    def check_num(self):
        id = self.user.id
        '''This function does not allow the user to have more than 5 stations saved.
        It deletes by the process of last in first out'''
        val = my_stations.objects.filter(user_id=id).count()
        if val > 3:
            all_ids = my_stations.objects.filter(user_id=id).values_list('id', flat=True)[1:3]
            my_stations.objects.filter(user_id=id).exclude(pk__in=list(all_ids)).delete()
