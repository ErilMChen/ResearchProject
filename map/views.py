from django.shortcuts import render
from itertools import chain
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from .models import *
import re
import json
from users.models import my_stations, my_plans
import users.views as uv
import users.forms as au
import weather.models as wm
from django.core import serializers
from map import get_prediction
#changes
import sys
from time import sleep
from django.views.decorators.csrf import csrf_exempt

def mobile(request):
    user_agent = request.META['HTTP_USER_AGENT']
    if 'Mobile' in user_agent:
        return True
    else:
        return False

# Create your views here.
def index(request):
	form1 = au.UserForm()
	form2 = au.AuthForm()

	if mobile(request) == True:
		return render(request, 'mindex.html', {"form1": form1, "form2": form2})
	return render(request, 'index.html', {"form1": form1, "form2": form2})

def BusStation(request):
	ret = BusStops.objects.values('stop_name','stop_lat','stop_long').distinct()
	data = list(ret)
	data = json.dumps(data)
	return HttpResponse(data)

def RouteDirection(request):
	start_stop = request.GET.get("start_stop","")
	if start_stop == 'My Location':
		my_loc = request.GET.get("my_loc", "")
		lat = float(my_loc.split("/")[0])
		long = float(my_loc.split("/")[1])
		print(lat, long)
		ret_start_stop = [{'stop_name': 'N/A', 'stop_lat': float(lat), 'stop_long': float(long)}]
		print(ret_start_stop)
	else:
		ret_start_stop = BusStops.objects.values('stop_name', 'stop_lat', 'stop_long').filter(
			stop_name=start_stop).distinct()

		print(ret_start_stop)

	end_stop = request.GET.get("end_stop","")
	date = request.GET.get("date","")
	time = request.GET.get("time","")

	ret_end_stop = BusStops.objects.values('stop_name','stop_lat','stop_long').filter(stop_name = end_stop).distinct()
	ret = chain(ret_start_stop, ret_end_stop)
	data = list(ret)
	data = json.dumps(data)
	return HttpResponse(data)

# machine learning interface
@csrf_exempt
def DurationPrediction(request):
	if(request.method == 'POST'):
		timeList = list()
		postBody = request.body
		json_result = json.loads(postBody)
		data = json_result['jsonArray']
		for route in data:
			try:
				origin_stop = route['startStop']
				dest_stop = route['endStop']
				bus_line = route['line']
				date = route['date']
				time = route['time']
			except:
				timeList.append("false")
				continue

			origin_digits_bool = re.findall("\d+", origin_stop)

			if origin_digits_bool:
				for num in origin_digits_bool:
					if ("top " + str(num)) in origin_stop:
						origin_stop = int(num)
			else:
				section_origin = origin_stop.split(",")
				origin_from_db = ""
				for section in section_origin:
					section = section.strip()
					origin_stop_line = str(section) + "_" + str(bus_line)
					try:
						origin_from_db = MatchStopNames.objects.values("stoppointid").filter(stop_name=origin_stop_line).distinct()[0]["stoppointid"]
					except:
						continue
				if origin_from_db:
					origin_stop = origin_from_db
				else:
					timeList.append("false")

			dest_digits_bool = re.findall("\d+", dest_stop)

			if dest_digits_bool:
				for num in dest_digits_bool:
					if ("top " + str(num)) in dest_stop:
						dest_stop = int(num)
			else:
				section_dest = dest_stop.split(",")
				dest_from_db = ""
				for section in section_dest:
					section = section.strip()
					dest_stop_line = str(section) + "_" + str(bus_line)
					try:
						dest_from_db = MatchStopNames.objects.values("stoppointid").filter(stop_name=dest_stop_line).distinct()[0]["stoppointid"]
					except:
						continue
				if dest_from_db:
					dest_stop = dest_from_db
				else:
					timeList.append("false")
					continue
			
			# predtime = origin_stop+ " " + dest_stop+ " " + bus_line+ " " + date+ " " + time
			predtime = get_prediction.get_prediction(origin_stop, dest_stop, bus_line, date, time)
			print(predtime)

			if predtime:
				timeList.append(predtime)
			else:
				timeList.append("false")

	res = json.dumps(timeList)
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
		ret = my_plans.objects.values('plan_name','start_stop','end_stop','date','time').filter(user=current_user).distinct()
		ret = my_plans.objects.values('plan_name','start_stop','end_stop','date','time','start_lat', 'start_long', 'end_lat', 'end_long').filter(user=current_user).distinct()
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
	# start_stop lat/lng, end_stop lat/lng  (double)
	slat = request.GET.get("slat","")
	slng = request.GET.get("slng","")
	elat = request.GET.get("elat","")
	elng = request.GET.get("elng","")

	if request.user.is_authenticated:
		res = json.dumps("true")
		current_user = request.user
		user_plan = my_plans(plan_name=plan_name, start_stop=start_stop,
						  end_stop=end_stop, date=date, time=time, user=current_user, start_lat= slat, start_long = slng, end_lat=elat,
							 end_long = elng)
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
		my_plans.objects.filter(plan_name=plan_name, start_stop=start_stop,
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
