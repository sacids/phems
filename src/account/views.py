from django.http import HttpResponseRedirect
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth.models import User, Group
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.conf import settings
from .forms import RegistrationForm
from utils import sendEmail

# user registration


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # save form in the memory not in database
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            # email and last name
            to_email = form.cleaned_data.get('email')
            surname = form.cleaned_data.get('last_name')

            # to get the domain of the current site
            current_site = get_current_site(request)

            # subject
            subject = 'Activation link has been sent to your email id'

            # message
            message = '<p>Dear <b>' + surname + '</b>, </p>'
            message += '<p>Please click on the link to confirm your registration<br/>' + \
                current_site + '</p>'

            message += '<p>If the above link is not clickable, please copy the whole link and paste it in your browser.</p>'

            # send email notification
            sendEmail(subject, message,
                      froEmail="afyadata@sacids.org", toEmail=[to_email])

            #group = Group.objects.get(name='student')

            # add user to a group
            # user.groups.add(group)

            #message and redirect
            messages.success(
                request, f'Your account has been created. You can log in now!')
            return redirect('login')
    else:
        form = RegistrationForm()

    context = {'form': form, 'title': 'Registration'}
    return render(request, 'register.html', context)


# login
def loginNow(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('admin')
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
                    return redirect('admin')
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
