from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import UserForm
import django.http.request as request
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
    return render(response, "users/users.html", {"form": form})


def login(response):
    if request.method == "POST":
        postdata = request.POST.copy()
        username = postdata.get('username', '')
        password = postdata.get('password', '')
        try:
            user = authenticate(username=username, password=password)
            login(request, user)
#    if response.method == 'POST':
#        form = UserForm(response.POST)
#        if form.is_valid():
            return redirect("/map")
        except Exception as e:
            print(e)