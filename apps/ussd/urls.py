from django.urls import path
from .views import *

urlpatterns = [
    path('tigo/', vodacom, name='tigo'),
    path('vodacom/', vodacom, name='vodacom'),
    path('halotel/', halotel, name='halotel'),
    path('zantel/', vodacom, name='zantel'),
    path('airtel/', vodacom, name='airtel'),
    
    
    path('some/url/', test_final_func, name="test_final_func"),
]