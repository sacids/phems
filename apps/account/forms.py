from dataclasses import fields
from django.forms.widgets import Textarea
import datetime
from datetime import timedelta
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from .models import Profile

class LoginForm(forms.Form):
    """Login form"""
    username = forms.CharField(max_length=30, required=True, label=False, widget=forms.TextInput(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5', 'placeholder': 'Write username...'}))
    password = forms.CharField(max_length=20, required=True, label=False, widget=forms.PasswordInput(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5', 'placeholder': 'Password...'}))

    class Meta: 
        fields = ('username', 'password')


class ProfileForm(forms.Form):
    """
    A class for profile
    """
    first_name = forms.CharField(max_length=30, required=True, label="Firstname ", widget=forms.TextInput(attrs={'class': 'w-full bg-white text-gray-600 border border-gray-300 rounded py-2.5 px-4 mb-3 my-1 focus:outline-none focus:border-none focus:bg-white text-sm font-normal', 'placeholder': 'Write first name...'}))
    last_name = forms.CharField(max_length=30, required=True, label="Lastname ", widget=forms.TextInput(attrs={'class': 'w-full bg-white text-gray-600 border border-gray-300 rounded py-2.5 px-4 mb-3 my-1 focus:outline-none focus:border-none focus:bg-white text-sm font-normal', 'placeholder': 'Write surname...'}))
    username = forms.CharField(max_length=30, required=True, label="Username ", widget=forms.TextInput(attrs={'class': 'w-full bg-white text-gray-600 border border-gray-300 rounded py-2.5 px-4 mb-3 my-1 focus:outline-none focus:border-none focus:bg-white text-sm font-normal', 'placeholder': 'Write username...'}))
    email = forms.EmailField(max_length=50, required=True, label="Email ", widget=forms.EmailInput(attrs={'class': 'w-full bg-white text-gray-600 border border-gray-300 rounded py-2.5 px-4 mb-3 my-1 focus:outline-none focus:border-none focus:bg-white text-sm font-normal', 'placeholder': 'Write email...'}))
    organization = forms.CharField(max_length=200, required=False, label="Organization ", widget=forms.TextInput(attrs={'class': 'w-full bg-white text-gray-600 border border-gray-300 rounded py-2.5 px-4 mb-3 my-1 focus:outline-none focus:border-none focus:bg-white text-sm font-normal', 'placeholder': 'Write organization...'}))
    title = forms.CharField(max_length=200, required=False, label="Title ", widget=forms.TextInput(attrs={'class': 'w-full bg-white text-gray-600 border border-gray-300 rounded py-2.5 px-4 mb-3 my-1 focus:outline-none focus:border-none focus:bg-white text-sm font-normal', 'placeholder': 'Write title...'}))
    postal_address = forms.CharField(max_length=200, required=False, label="Postal address ", widget=forms.TextInput(attrs={'class': 'w-full bg-white text-gray-600 border border-gray-300 rounded py-2.5 px-4 mb-3 my-1 focus:outline-none focus:border-none focus:bg-white text-sm font-normal', 'placeholder': 'Write postal address...'}))

    class Meta:
        fields = ('first_name', 'last_name', 'email', 'username', 'organization', 'title', 'postal_address' )


class ChangePasswordForm(PasswordChangeForm):
    """Change password form"""
    old_password = forms.CharField(max_length=30, required=True, label="Old Password ", widget=forms.PasswordInput(attrs={'class': 'w-full bg-white text-gray-600 border border-gray-300 rounded py-2.5 px-4 mb-3 my-1 focus:outline-none focus:border-none focus:bg-white text-sm font-normal', 'placeholder': 'Write old password...'}))
    new_password1 = forms.CharField(max_length=30, required=True, label="New Password ", widget=forms.PasswordInput(attrs={'class': 'w-full bg-white text-gray-600 border border-gray-300 rounded py-2.5 px-4 mb-3 my-1 focus:outline-none focus:border-none focus:bg-white text-sm font-normal', 'placeholder': 'New password...'}))
    new_password2 = forms.CharField(max_length=30, required=True, label="Confirm Password ", widget=forms.PasswordInput(attrs={'class': 'w-full bg-white text-gray-600 border border-gray-300 rounded py-2.5 px-4 mb-3 my-1 focus:outline-none focus:border-none focus:bg-white text-sm font-normal', 'placeholder': 'Confirm new password...'}))

    class Meta: 
        fields = ('old_password', 'new_password1', 'new_password2')


class UserForm(UserCreationForm):
    """User Form"""
    first_name = forms.CharField(max_length=50, label="First Name ", widget=forms.TextInput(attrs={'class': 'w-full bg-white text-gray-600 border border-gray-200 rounded p-2.5 mb-3 my-1 focus:outline-none focus:border-blue-900 focus:bg-white text-sm font-normal', 'placeholder': 'Write first name...'}))
    last_name = forms.CharField(max_length=50, label="Last Name ", widget=forms.TextInput(attrs={'class': 'w-full bg-white text-gray-600 border border-gray-200 rounded p-2.5 mb-3 my-1 focus:outline-none focus:border-blue-900 focus:bg-white text-sm font-normal', 'placeholder': 'Write surname...'}))
    username = forms.CharField(max_length=100, label="Username ", widget=forms.TextInput(attrs={'class': 'w-full bg-white text-gray-600 border border-gray-200 rounded p-2.5 mb-3 my-1 focus:outline-none focus:border-blue-900 focus:bg-white text-sm font-normal', 'placeholder': 'Write username...'}))
    email = forms.EmailField(max_length=100, label="Email ", widget=forms.EmailInput(attrs={'class': 'w-full bg-white text-gray-600 border border-gray-200 rounded p-2.5 mb-3 my-1 focus:outline-none focus:border-blue-900 focus:bg-white text-sm font-normal', 'placeholder': 'Write email...'}))
    password1 = forms.CharField(max_length=20, label="Password ", widget=forms.PasswordInput(attrs={'class': 'w-full bg-white text-gray-600 border border-gray-200 rounded p-2.5 mb-3 my-1 focus:outline-none focus:border-blue-900 focus:bg-white text-sm font-normal', 'placeholder': 'Password...'}))
    password2 = forms.CharField(max_length=20, label="Confirm Password ", widget=forms.PasswordInput(attrs={'class': 'w-full bg-white text-gray-600 border border-gray-200 rounded p-2.5 mb-3 my-1 focus:outline-none focus:border-blue-900 focus:bg-white text-sm font-normal', 'placeholder': 'Confirm password...'}))

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['username'].required = True
        self.fields['email'].required = True
        self.fields['password1'].required = True
        self.fields['password2'].required = True

        if self.instance.pk:
            self.fields['username'].required = False
            self.fields['email'].required = False
            self.fields['password1'].required = False
            self.fields['password2'].required = False

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2',)


class UserUpdateForm(UserChangeForm):
    """User Form"""
    first_name = forms.CharField(max_length=50, label="First Name", widget=forms.TextInput(attrs={'class': 'w-full bg-white text-gray-600 border border-gray-200 rounded p-2.5 mb-3 my-1 focus:outline-none focus:border-blue-900 focus:bg-white text-sm font-normal', 'placeholder': 'Write first name...'}))
    last_name = forms.CharField(max_length=50, label="Last Name", widget=forms.TextInput(attrs={'class': 'w-full bg-white text-gray-600 border border-gray-200 rounded p-2.5 mb-3 my-1 focus:outline-none focus:border-blue-900 focus:bg-white text-sm font-normal', 'placeholder': 'Write surname...'}))
    username = forms.CharField(max_length=100, label="Username", widget=forms.TextInput(attrs={'class': 'w-full bg-white text-gray-600 border border-gray-200 rounded p-2.5 mb-3 my-1 focus:outline-none focus:border-blue-900 focus:bg-white text-sm font-normal', 'placeholder': 'Write username...'}))
    email = forms.EmailField(max_length=100, label="Email", widget=forms.EmailInput(attrs={'class': 'w-full bg-white text-gray-600 border border-gray-200 rounded p-2.5 mb-3 my-1 focus:outline-none focus:border-blue-900  focus:bg-white text-sm font-normal', 'placeholder': 'Write email...'}))

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)

        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['username'].required = True
        self.fields['email'].required = True

        if self.instance.pk:
            self.fields['username'].required = False
            self.fields['email'].required = True

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username',)


class UserProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['sector'].empty_label = '-- Select --'
        self.fields['sector'].required = True
        self.fields['level'].required = True

    class Meta:
        model = Profile
        fields = ('sector', 'organization', 'level', 'phone', 'title', 'postal_address')

        widgets = {
            'sector': forms.Select(attrs={'class': 'w-full bg-white text-gray-600 border border-gray-200 rounded p-2.5 mb-3 my-1 focus:outline-none focus:border-blue-900 focus:bg-white text-sm font-normal', 'id': 'sector' }),
            'phone': forms.TextInput(attrs={'class': 'w-full bg-white text-gray-600 border border-gray-200 rounded p-2.5 mb-3 my-1 focus:outline-none focus:border-blue-900 focus:bg-white text-sm font-normal', 'id': 'phone', 'placeholder': 'Write phone...' }),
            'organization': forms.TextInput(attrs={'class': 'w-full bg-white text-gray-600 border border-gray-200 rounded p-2.5 mb-3 my-1 focus:outline-none focus:border-blue-900 focus:bg-white text-sm font-normal', 'id': 'organization', 'placeholder': 'Write organization...' }),
            'title': forms.TextInput(attrs={'class': 'w-full bg-white text-gray-600 border border-gray-200 rounded p-2.5 mb-3 my-1 focus:outline-none focus:border-blue-900 focus:bg-white text-sm font-normal', 'id': 'title', 'placeholder': 'Write title...' }),
            'postal_address': forms.TextInput(attrs={'class': 'w-full bg-white text-gray-600 border border-gray-200 rounded p-2.5 mb-3 my-1 focus:outline-none focus:border-blue-900 focus:bg-white text-sm font-normal', 'id': 'postal_address', 'placeholder': 'Write postal address...' }),
            'level': forms.Select(attrs={'class': 'w-full bg-white text-gray-600 border border-gray-200 rounded p-2.5 mb-3 my-1 focus:outline-none focus:border-blue-900 focus:bg-white text-sm font-normal', 'id': 'level', }),
        }

        labels = {
            'sector': 'Primary Sector ',
            'organization': 'Organization ',
            'level': 'User Level ',
            'title': 'Title ',
            'postal_address': 'Postal address ',
        }
