from django.urls import path

from . import views
from users import views as uv

urlpatterns = [
    path('', views.index, name='index'),
    path('busstation', views.BusStation, name='busstation'),
    path('route/', views.RouteDirection, name="routedirection"),
    path('', uv.extra, name="login"),
]