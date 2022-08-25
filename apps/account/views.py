from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import View, UpdateView
from .forms import RegistrationForm, LoginForm
from django.contrib.auth.models import User
from .models import Profile

from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from .tokens import account_activation_token

from django.contrib.auth import login, authenticate, logout
from django.conf import settings
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode


# Register View
class RegistrationView(View):
    form_class = RegistrationForm
    template_name = 'register.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():

            user = form.save(commit=False)
            user.is_active = False  # Deactivate account till it is confirmed
            user.save()

            current_site = get_current_site(request)
            subject = 'Activate Account'
            message = render_to_string('emails/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)

            # message
            messages.success(
                request, ('Please Confirm your email to complete registration.'))

            # redirect
            return redirect('login')

        # render
        return render(request, self.template_name, {'form': form})

# login


class LoginView(View):
    form_class = LoginForm
    template_name = 'login.html'
    success_url = 'dashboard'

    def get(self, request, *args, **kwargs):
        form = LoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = LoginForm(data=request.POST)
        
        if form.is_valid():
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
                return redirect(self.success_url)
            else:
                messages.error(request, 'Wrong credentials, try again!')

       # render
        return render(request, self.template_name, {'form': form})


# Logout
class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.error(request, 'Log out successfully')
        return redirect('login')


# Activate account
class ActivateAccount(View):
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.profile.email_verified = True
            user.save()
            login(request, user)
            messages.success(request, ('Your account have been confirmed.'))
            return redirect('login')
        else:
            messages.warning(
                request, ('The confirmation link was invalid, possibly because it has already been used.'))
            return redirect('login')



