from django.urls import path
from .views import *

urlpatterns = [
    path('halotel/', soap_rec, name='halotel'),
    path('smpp/', smpp_rec, name='zantel'),
    
]