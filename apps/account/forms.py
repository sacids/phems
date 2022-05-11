from dataclasses import fields
from django.forms.widgets import Textarea
import datetime
from datetime import timedelta
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

# User registration
class RegistrationForm(UserCreationForm):
    """
    A class to create traveller form.
    """
    first_name = forms.CharField(max_length=30, required=True, label=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Write first name...'}))
    last_name = forms.CharField(max_length=30, required=True, label=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Write surname...'}))
    username = forms.CharField(max_length=30, required=True, label=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Write username...'}))
    email = forms.EmailField(max_length=50, required=True, label=False, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Write email...'}))
    password1 = forms.CharField(max_length=20, required=True, label=False, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password...'}))
    password2 = forms.CharField(max_length=20, required=True, label=False, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm password...'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2', )


#user login
class LoginForm(forms.Form):
    username = forms.CharField(max_length=30, required=True, label=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Write username...'}))
    password = forms.CharField(max_length=20, required=True, label=False, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password...'}))

    class Meta: 
        fields = ('username', 'password')
