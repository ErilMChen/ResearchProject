from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from .models import MyUser
#from django.contrib.auth.models import User

class UserForm(UserCreationForm):
    """This is the form used to create MyUsers"""
    email = forms.EmailField()

    class Meta:
        model = MyUser
        fields = ["email", "password1"]

class AuthForm(AuthenticationForm):
    """This is the form used to log in MyUsers"""
    #email = forms.EmailField()
    class Meta:
        model = MyUser
        fields = ['email', 'password']