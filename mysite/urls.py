"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from users import views as v_users
from favourites import views as f_views
from tastypie.api import Api
from tastypie.api import Api
from api.resources import MyModelResource, BusModelResources

v1_api = Api(api_name='v1')
v1_api.register(MyModelResource())
v1_api.register(BusModelResources())

urlpatterns = [
    path('map/', include('map.urls')),
    path('admin/', admin.site.urls),
    path('users/', v_users.users, name='users'),
    path('login/', v_users.login, name='login'),
    path('mystations/', f_views.stations, name='mystations'),
    path('mystations/show_favs', f_views.show_favs, name='show_favs/'),
    path('delete_my_stop/', f_views.delete_my_stop, name='/delete_my_stop/'),
    path('logout/', v_users.logoutUser, name='/logout/'),
    path('changepass/', f_views.change_password, name='/changepass/'),
    path('delete_acc/', v_users.delete_acc, name = '/delete_acc'),
    path('api/', include(v1_api.urls)),
]
