from django.urls import path, include
from rest_framework import routers
from django.urls.resolvers import URLPattern
from .views import *
from . import api


router = routers.DefaultRouter()
router.register(r'signal', api.SignalViewSet)


urlpatterns = [
    path('', include(router.urls)),
]