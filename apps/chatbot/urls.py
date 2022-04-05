from django.urls import path
from django.urls.resolvers import URLPattern
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("whatsapp/", whatsapp, name="whatsapp"),
    path("telegram/", telegram, name="telegram"),
]