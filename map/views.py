from django.shortcuts import render
from itertools import chain
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from .models import *
import json

import users.views as uv
import users.forms as au

# Create your views here.
def index(request):
	form1 = au.UserForm()
	form2 = au.AuthForm()
	return render(request, 'index.html', {"form1": form1, "form2": form2})

def BusStation(request):
	ret = BusStops.objects.values('stop_name','stop_lat','stop_long').distinct()
	ret = MapAllroutedata.objects.values('shortcommonname_en','latitude','longitude').distinct()
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
	ret_start_stop = MapAllroutedata.objects.values('shortcommonname_en','latitude','longitude').filter(shortcommonname_en = start_stop).distinct()
	ret_end_stop = MapAllroutedata.objects.values('shortcommonname_en','latitude','longitude').filter(shortcommonname_en = end_stop).distinct()
	ret = ret_start_stop | ret_end_stop

	data = list(ret)
	data = json.dumps(data)
	return HttpResponse(data)

def login(response):
    uv.login(response)

def users(response):
    uv.users(response)

def extra(response):
    uv.extra(response)