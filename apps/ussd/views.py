from django.shortcuts import render
import json
import requests
from .ussd_lib import ussd_session
from .models import *
from django.db.models import Q
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect

# Create your views here.
def vodacom(request):
    
    session_id      = request.GET['session_id']
    msisdn          = request.GET['msisdn']
    msg             = request.GET['msg']
    #msg_type        = request.GET['type']
    
    
    j = ussd_session(session_id,msisdn,msg)
    response = j.get_response()
    
    return JsonResponse(response['msg'], safe=False)
    
 

def test_final_func(request):
    current_url = request.build_absolute_uri()
    print(current_url)
    return JsonResponse(1, safe=False)
    
     
     
     
   