from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import MyUser

# Register your models here.
@admin.register(MyUser)
class MyAdmin(admin.ModelAdmin):
    pass


#admin.site.register(MyUser)