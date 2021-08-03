from django.shortcuts import render
from itertools import chain
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from .models import *
import json
from users.models import my_stations, plans
import users.views as uv
import users.forms as au
import weather.models as wm
from django.core import serializers
from map import get_prediction


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

# machine learning interface
def DurationPrediction(request):
	origin_stop = request.GET.get("start_stop","")
	dest_stop = request.GET.get("end_stop","")
	headsign = request.GET.get("line_name","")
	bus_line = request.GET.get("line","")
	date = request.GET.get("date","")
	time = request.GET.get("time","")
	origin_stop = BusStops.objects.values('stoppointid').filter(stop_name = origin_stop).distinct()
	dest_stop = BusStops.objects.values('stoppointid').filter(stop_name = dest_stop).distinct()
	print(origin_stop[0]["stoppointid"], dest_stop[0]["stoppointid"], bus_line, headsign, date, time)
	predtime = get_prediction.get_prediction(origin_stop[0]["stoppointid"], dest_stop[0]["stoppointid"], bus_line, date, time)
	print(predtime)

	res = json.dumps(predtime)
	return HttpResponse(res)

def GetUserStatus(request):
	if request.user.is_authenticated:
		res = json.dumps("true")
	else:
		res = json.dumps("false")
	return HttpResponse(res)

# scy plan
def LoadPlan(request):
	if request.user.is_authenticated:
		current_user = request.user
		ret = plans.objects.values('plan_name','start_stop','end_stop','date','time').filter(user=current_user).distinct()
		data = list(ret)
		data = json.dumps(data)
		return HttpResponse(data)
	else:
		res = json.dumps()
		return HttpResponse(res)

# save plan into database 
def AddPlan(request):
	plan_name = request.GET.get("plan_name","")
	start_stop = request.GET.get("start_stop","")
	end_stop = request.GET.get("end_stop","")
	date = request.GET.get("date","")
	time = request.GET.get("time","")


	if request.user.is_authenticated:
		res = json.dumps("true")
		current_user = request.user
		user_plan = plans(plan_name=plan_name, start_stop=start_stop,
						  end_stop=end_stop, date=date, time=time, user=current_user)
		user_plan.check_num_plans()
		user_plan.save()
		print('success')

	else:
		res = json.dumps("false")
	return HttpResponse(res)	

# delete plan from database 
def DeletePlan(request):
	plan_name = request.GET.get("plan_name","")
	start_stop = request.GET.get("start_stop","")
	end_stop = request.GET.get("end_stop","")
	date = request.GET.get("date","")
	time = request.GET.get("time","")

	print(plan_name + start_stop + end_stop + date + time)

	if request.user.is_authenticated:
		res = json.dumps("true")
		current_user = request.user
		plans.objects.filter(plan_name=plan_name, start_stop=start_stop,
							 end_stop=end_stop, date=date, time=time, user=current_user).delete()
		print('delete success')
	else:
		res = json.dumps("false")
	return HttpResponse(res)

def AddFavoriteStop(request):

	stop = request.GET.get("stop_name","")
	ret1 = BusStops.objects.values('stop_name','routes_serving').filter(stop_name = stop).distinct()
	ret2 = NameToID.objects.values('stop_name','stop_id').filter(stop_name = stop).distinct()
	data1 = list(ret1)
	data2 = list(ret2)

	stop_name = data1[0]['stop_name']
	route_nums = data1[0]['routes_serving'].split(',')
	stop_id = data2[0]['stop_id']
	if request.user.is_authenticated:
		current_user = request.user
		print('user id', current_user.id)
		stop_name = data1[0]['stop_name']
		route_nums = data1[0]['routes_serving'].split(',')
		stop_id = data2[0]['stop_id']
		user_fav = my_stations(stop_id=stop_id, user=current_user)
		user_fav.check_num()
		user_fav.save()
		res = json.dumps("true")
	else:
		print('not logged in')
		res = json.dumps("false")
		pass

	return HttpResponse(res)


def get_live_updates(response):
	x = wm.AA_Road_Report.objects.all()
	road_updates = serializers.serialize("json", wm.AA_Road_Report.objects.all())
	#print(road_updates)
	return HttpResponse(road_updates, "application/json")
