from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth.models import User, Group
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.conf import settings
from .forms import RegistrationForm

# user registration
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()

            #group = Group.objects.get(name='student') 

            #add user to a group      
            #user.groups.add(group)

            #message and redirect
            messages.success(request, f'Your account has been created. You can log in now!')    
            return redirect('login')
    else:
        form = RegistrationForm()

    context = {'form': form, 'title': 'Registration'}
    return render(request, 'register.html', context)


# login
def loginNow(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect ('admin')
        else:   
            return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            # authenticate user
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)

                remember_me = request.POST.get("remember_me")
                if remember_me is True:
                    ONE_MONTH = 30 * 24 * 60 * 60
                    expiry = getattr(
                        settings, "KEEP_LOGGED_DURATION", ONE_MONTH)
                    request.session.set_expiry(expiry)

                # redirect
                if request.user.is_superuser:
                    return redirect ('admin')
                else:   
                    return redirect('home')
            else:
                messages.error(request, 'Username or password incorectly')

        context = {'title': 'Login'}
        return render(request, 'login.html', context)


# logout
def logoutNow(request):
    logout(request)
    messages.error(request, 'Log out successfully')
    return redirect('login')