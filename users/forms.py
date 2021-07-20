from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import (
    AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm,
)
from django import forms
from .models import MyUser
from django.contrib.auth.hashers import make_password, check_password

#from django.contrib.auth.models import User

class UserForm(UserCreationForm):
    """This is the form used to create MyUsers"""
    email = forms.EmailField()


    class Meta:
        model = MyUser
        fields = ["email", "name", "password1"]


class AuthForm(AuthenticationForm):
    """This is the form used to log in MyUsers"""
    #email = forms.EmailField()
    class Meta:
        model = MyUser
        fields = ['email', 'password']

class MyLoginView(LoginView):
    authentication_form = AuthForm


class ChangePassword(PasswordResetForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'type':'password'}))
    new_password =  forms.CharField(widget=forms.PasswordInput(attrs={ 'class': 'form-control','type':'password'}))
    reenter_password =  forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','type':'password'}))

    def clean_confirm_password(self):
        cleaned_data = super(ChangePassword, self).clean()
        new_password = self.cleaned_data.get('new_password')
        reenter_password = self.cleaned_data.get('reenter_password')
        old_password = self.cleaned_data.get('old_password')

        if new_password and new_password != reenter_password or new_password == old_password or len(new_password) < 8:
            raise ValidationError("Passwords are not matching or have been used before. Try again.")
        return new_password

    class Meta:
        model = MyUser
        fields = ['old_password', 'new_password', 'reenter_password']