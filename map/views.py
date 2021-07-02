from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from .models import *
import json

# Create your views here.
def index(request):
    return render(request, 'index.html')

def BusStation(request):
	ret = MapAllroutedata.objects.values('shortcommonname_en','latitude','longitude').distinct()
	data = list(ret)
	data = json.dumps(data)
	return HttpResponse(data)

def RouteDirection(request):
	start_stop = request.GET.get("start_stop","")
	end_stop = request.GET.get("end_stop","")
	ret_start_stop = MapAllroutedata.objects.values('shortcommonname_en','latitude','longitude').filter(shortcommonname_en = start_stop).distinct()
	ret_end_stop = MapAllroutedata.objects.values('shortcommonname_en','latitude','longitude').filter(shortcommonname_en = end_stop).distinct()
	ret = ret_start_stop | ret_end_stop
	data = list(ret)
	data = json.dumps(data)
	return HttpResponse(data)