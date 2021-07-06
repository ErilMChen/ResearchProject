from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import UserForm, AuthForm
import django.http.request as request
from django.contrib.auth import authenticate, get_user_model
#from .models import MyUser

# Create your views here.
def users(response):
    if response.method == 'POST':
        form = UserForm(response.POST)
        user = form.save(commit=False)
        if form.is_valid():
            user.set_password(form.cleaned_data['password1'])
            user.save()
            return redirect("/map")
    else:
        form = UserForm()
    return render(response, "map/index.html", {"form": form})


def login(response):
    if response.method == "POST":
        postdata = response.POST.copy()
        email = postdata.get('email', '')
        password = postdata.get('password', '')
        try:
            user = authenticate(email=email, password=password)
            login(request, user)
            return redirect("/test")
        except Exception as e:
            print(e)

def extra(response):
    form1 = UserForm()
    form2 = AuthForm()
    return (response, "map/index.html", {"form1": form1, "form2": form2})
