from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login as LOG
from .forms import UserForm, AuthForm
from django.contrib.auth import authenticate
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
                mess = messages.success(response, 'Your account has been made and you are logged in. Add favourite stops and access' +
                                 ' your favourite stations profile page.')
                user = authenticate(username=email, password=p)
                if user is not None:
                    LOG(response, user)
                return redirect('/map')
        else:
            mess = messages.error(response, 'Account failed. Email may be in use, passwords may not match or may be too short.')
            return redirect('/map')

    else:
        form1 = UserForm()
        form2 = AuthForm()
        return (response, "map/index.html", {"form1": form1, "form2": form2})


def login(response):
    """Allows users to log in"""
    if response.method == "POST":
        try:
            email = response.POST['username']
            password = response.POST['password']
            print(email, password)
            user = authenticate(username=email, password=password)
            if user is not None:
                LOG(response, user)
            else:
                mess = messages.error(response, 'Login Failed. Check your credentials.')
                return redirect('/map')
        except Exception as e:
            print(e)
            return redirect('/map')
    return redirect("/map")

def extra(response):
    '''Render both forms for login and sign up on the index page'''
    form1 = UserForm()
    form2 = AuthForm()
    return (response, "map/index.html", {"form1": form1, "form2": form2})


def logoutUser(request):
    logout(request)
    return redirect("/map")