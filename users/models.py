from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class MyUserManger(BaseUserManager):
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
        return self.name

    def has_module_perms(self, perm, obj=None):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return self.is_admin

class favourite_place(models.Model):
    place_name = models.CharField(max_length=50)
    latitude = models.FloatField()
    longitude = models.FloatField()
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.name + ": " + self.place_name