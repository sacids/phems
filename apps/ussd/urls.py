from django.urls import path
from .views import *

urlpatterns = [
    path('tigo/', tigo, name='tigo'),
    path('vodacom/', vodacom, name='vodacom'),
    path('halotel/', halotel, name='halotel'),
    path('zantel/', vodacom, name='zantel'),
    path('ttcl/', ttcl, name='ttcl'),
    
    
    path('some/url/', test_final_func, name="test_final_func"),
    path('return/param/', return_param, name="return_param"),
]