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
from django.contrib.auth import views as a_views
from users import views as v_users
from favourites import views as f_views

urlpatterns = [
    path('map/', include('map.urls')),
    path('admin/', admin.site.urls),
    path('users/', v_users.users, name='users'),
    path('login/', a_views.LoginView.as_view(template_name='users/login.html'),name='login'),
    path('test/', v_users.extra, name='test'),
    path('mystations/', f_views.stations, name='mystations'),
    path('mystations_auth/', f_views.check_auth, name='mystations_auth'),
    path('mystations_auth/show_favs/', f_views.show_favs, name='show_favs/')
   #path('test/', a_views.LoginView.as_view(template_name='users/test.html'), name='test'),
]
