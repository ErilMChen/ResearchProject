from django.shortcuts import render, redirect, HttpResponse
from users.models import my_stations
# Create your views here.
from favourites import get_sched2
import json
from ast import literal_eval


def stations(request):
	return render(request, 'mystations.html')

def check_auth(request):
    if request.user.is_authenticated:
        current_user = request.user
        station_id = '8220DB007739'
        user_fav = my_stations(stop_id = station_id, user = current_user)
        user_fav.save()
        return render(request, 'mystations.html')
    else:
        ## do soemthing else
        return render(request, 'mystations.html')


def show_favs(request):
    if request.user.is_authenticated:
        data = []
        current_user = request.user
        stations = my_stations.objects.filter(user=current_user).values('stop_id').distinct()
        print(stations)
        for row in stations:
            stop = row['stop_id']
            s = get_sched2.get_times(stop)
            data.append(s)
        data = json.dumps(data)
        return HttpResponse(data, "application/json")

