from django.urls import path
from django.urls.resolvers import URLPattern
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("subscription/", subscription, name="subscribe"),
    path("push/", send_push, name="push"),
]