from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from users.models import my_stations
# Create your views here.
from favourites import get_sched2
from django.views.decorators.csrf import csrf_exempt
from .forms import StopForm as S
from users.forms import ChangePassword
from users.models import MyUser

import re
from django.views.decorators.cache import never_cache

#https://stackoverflow.com/questions/42273319/detect-mobile-devices-with-django-and-python-3
def mobile(request):
    user_agent = request.META['HTTP_USER_AGENT']
    if 'Mobile' in user_agent:
        return True
    else:
        return False
@never_cache
def stations(request):
    """Sends the delete stop form to stations.html and render template"""
    myform = S
    change_pass = ChangePassword
    if mobile(request) == True:
        return render(request, 'stations_mob.html', {"form1": myform, "form2": change_pass})
    else:
        return render(request, 'mystations.html', {"form1": myform, "form2": change_pass})


def show_favs(request):
    """When stations.html is rendered, the live schedule for the
    users favourite stations are returned from get_sched2 file and are sent to front end as json"""
    if request.user.is_authenticated:
        current_user = request.user
        stations = my_stations.objects.filter(user=current_user).values_list('stop_id', flat=True).distinct()
        s = get_sched2.get_times(stations)
        data.append(s)
        #print(data)
        return HttpResponse(data, "application/json")

@csrf_exempt
def delete_my_stop(request):
    """Allows user to delete a stop using the form rendered in stations(request)"""
    if request.method == 'POST':
        current_user = request.user
        postdata = request.POST.copy()
        station = postdata.get('name', '')
        delete_stop(station, current_user)
        print(station, "is station")
    return HttpResponseRedirect('/mystations/')

def delete_stop(station, user):
    """Deletes the stop"""
    my_stations.objects.filter(user=user, stop_id=station).delete()
    return

def change_password(request):
    if request.method == 'POST':
        current_user = request.user
        form = ChangePassword(request.POST)
        try:
            if form.is_valid():
                new_p = form.clean_confirm_password()
                user = MyUser.objects.get(id=current_user.id)
                user.set_password(new_p)
                print('set')
                user.save()
                return HttpResponse('Password has been changed')
            else:
                print('invalid')
                return HttpResponse('Password has not been changed. Check your credentials.')
        except:
            return HttpResponse('Password has not been changed. Check your credentials.')
