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
    username = forms.CharField(max_length=30, required=True, label=False, widget=forms.TextInput(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500', 'placeholder': 'Write username...'}))
    password = forms.CharField(max_length=20, required=True, label=False, widget=forms.PasswordInput(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500', 'placeholder': 'Password...'}))

    class Meta: 
        fields = ('username', 'password')
