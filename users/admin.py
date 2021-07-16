from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import MyUser

class UserAdmin(UserAdmin):
    ## pick how we want to see the views on the admin
    ordering = ('email',)
    list_display = ('email', 'is_staff', )
    search_fields = ('email', )
    # dont want to be able to change ID as its a foreign key
    readonly_fields = ('id',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()



admin.site.register(MyUser, UserAdmin)