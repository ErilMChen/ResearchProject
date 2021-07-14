from django.urls import path

from . import views
from users import views as UV

urlpatterns = [
    path('', views.index, name='index'),
    path('get_live_updates', views.get_live_updates, name='updates'),
    path('busstation', views.BusStation, name='busstation'),
    path('route/', views.RouteDirection, name="routedirection"),
    path('add/', views.AddFavoriteStop, name="routedirection"),
    path('plan/', views.AddPlan, name="addplan"),
    path('status', views.GetUserStatus, name="userstatus"),

]