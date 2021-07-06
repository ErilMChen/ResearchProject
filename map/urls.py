from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('busstation', views.BusStation, name='busstation'),
    path('route/', views.RouteDirection, name="routedirection"),
    path('add/', views.AddFavoriteStop, name="routedirection"),
]