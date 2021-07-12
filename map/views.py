from django.shortcuts import render
from itertools import chain
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from .models import *
import json
from users.models import my_stations
import users.views as uv
import users.forms as au

# Create your views here.
def index(request):
	form1 = au.UserForm()
	form2 = au.AuthForm()
	return render(request, 'index.html', {"form1": form1, "form2": form2})

def BusStation(request):
	ret = BusStops.objects.values('stop_name','stop_lat','stop_long').distinct()
	data = list(ret)
	data = json.dumps(data)
	return HttpResponse(data)

def RouteDirection(request):
	start_stop = request.GET.get("start_stop","")
	end_stop = request.GET.get("end_stop","")
	date = request.GET.get("date","")
	time = request.GET.get("time","")
	ret_start_stop = BusStops.objects.values('stop_name','stop_lat','stop_long').filter(stop_name = start_stop).distinct()
	ret_end_stop = BusStops.objects.values('stop_name','stop_lat','stop_long').filter(stop_name = end_stop).distinct()
	ret = chain(ret_start_stop, ret_end_stop)
	data = list(ret)
	data = json.dumps(data)
	return HttpResponse(data)

def AddPlan(request):
	plan_name = request.GET.get("plan_name","")
	start_stop = request.GET.get("start_stop","")
	end_stop = request.GET.get("end_stop","")
	date = request.GET.get("date","")
	time = request.GET.get("time","")
	


def AddFavoriteStop(request):

	stop = request.GET.get("stop_name","")
	ret1 = BusStops.objects.values('stop_name','routes_serving').filter(stop_name = stop).distinct()
	ret2 = NameToID.objects.values('stop_name','stop_id').filter(stop_name = stop).distinct()
	data1 = list(ret1)
	data2 = list(ret2)

	if request.user.is_authenticated:
		current_user = request.user
		stop_name = data1[0]['stop_name']
		print(stop_name)
		route_nums = data1[0]['routes_serving'].split(',')
		print(route_nums)
		stop_id = data2[0]['stop_id']
		print(stop_id)
		user_fav = my_stations(stop_id=stop_id, user=current_user)
		user_fav.check_num()
		user_fav.save()

	else:
		print('not logged in')
		pass

	# return HttpResponse(data1)

def login(response):
    uv.login(response)

def users(response):
    uv.users(response)

def extra(response):
    uv.extra(response)