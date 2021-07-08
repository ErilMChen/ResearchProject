from django.shortcuts import render, redirect, HttpResponse
from users.models import my_stations
# Create your views here.
from favourites import get_sched2
from django.views.decorators.csrf import csrf_exempt
from .forms import StopForm as S

def stations(request):
    myform = S
    return render(request, 'mystations.html', {"form1": myform})

def check_auth(request):
    if request.user.is_authenticated:
        current_user = request.user
        station_id = '8220DB000326'
        user_fav = my_stations(stop_id = station_id, user = current_user)
        user_fav.check_num()
        user_fav.save()
        return render(request, 'mystations.html')
    else:
        ## do soemthing else
        return render(request, 'mystations.html')


def show_favs(request):
    if request.user.is_authenticated:
        data = []
        current_user = request.user
        stations = my_stations.objects.filter(user=current_user).values_list('stop_id', flat=True).distinct()
        s = get_sched2.get_times(stations)
        data.append(s)
        print(data)
        return HttpResponse(data, "application/json")

@csrf_exempt
def delete_my_stop(request):
    if request.method == 'POST':
        postdata = request.POST.copy()
        station = postdata.get('name', '')
        print(type(station))
        print(station, "is station")
    return render(request, 'mystations.html')