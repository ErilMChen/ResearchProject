from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from users.models import my_stations
# Create your views here.
from favourites import get_sched2
from django.views.decorators.csrf import csrf_exempt
from .forms import StopForm as S
from users.forms import ChangePassword
from users.models import MyUser



def stations(request):
    """Sends the delete stop form to stations.html and render template"""
    myform = S
    change_pass = ChangePassword
    return render(request, 'mystations.html', {"form1": myform, "form2": change_pass})

def check_auth(request):
    """Checks if user is authenticated. (((( NOT NEEDED))))"""
    if request.user.is_authenticated:
        current_user = request.user
        station_id = '8240DB000231'
        user_fav = my_stations(stop_id = station_id, user = current_user)
        user_fav.check_num()
        user_fav.save()
        return HttpResponseRedirect('/mystations/')
    else:
        ## do soemthing else
        return HttpResponseRedirect('/mystations/')


def show_favs(request):
    """When stations.html is rendered, the live schedule for the
    users favourite stations are returned from get_sched2 file and are sent to front end as json"""
    if request.user.is_authenticated:
        data = []
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