from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib import messages
from django.conf import settings
from django.contrib.auth import login as LOG, authenticate
from .forms import UserForm, AuthForm
import django.http.request as request
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth import logout
from users.models import MyUser

# Create your views here.
def users(response):
    """Allows users to create a profile"""
    if response.method == 'POST':
        form = UserForm(response.POST)
        if form.is_valid():
            user = form.save(commit=False)
            email = form.cleaned_data['email']
            p = form.cleaned_data['password1']
            user.set_password(p)
            if MyUser.objects.filter(email=email).count() == 0:
                user.save()
                mess = messages.success(response, 'Your account has been made! Log in to add favourite stops and access' +
                                 ' your favourite stations profile page')
                return redirect('/map')
        else:
            mess = messages.error(response, 'Account failed. Email ay be in use, passwords may not match or may be too short.')
            return redirect('/map')

    else:
        form1 = UserForm()
        form2 = AuthForm()
        return (response, "map/index.html", {"form1": form1, "form2": form2})


def login(response):
    """Allows users to log in"""
    if response.method == "POST":
        form = AuthForm(response.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(email=email, password=password)
            #LOG(request, user)
            if user is not None:  # Verify form's content existence
                LOG(request, user)
                return redirect("/map")
    return redirect('/map')

def extra(response):
    '''Render both forms for login and sign up on the index page'''
    form1 = UserForm()
    form2 = AuthForm()
    return (response, "map/index.html", {"form1": form1, "form2": form2})


def logoutUser(request):
    logout(request)
    return redirect("/map")


def login_failed(request):
    if request.user.is_authenticated:
        pass
    else:
        mess = messages.error(request, 'Login Failed. Check your credentials.')
    return redirect('/map')