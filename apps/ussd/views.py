from django.shortcuts import render
import json
import requests
from .ussd_lib import ussd_session
from .models import *
from django.db.models import Q
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect



#halotel
from django.views.decorators.csrf import csrf_exempt
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

from .tasks import send_response


# Create your views here.
def vodacom(request):
    
    session_id      = request.GET['session_id']
    msisdn          = request.GET['msisdn']
    msg             = request.GET['msg']
    msg_type        = request.GET['type']
    
    ussd_trx = ussd_session(session_id,msisdn,msg)
    
    
    if msg_type == '3' or msg_type == '4' or msg_type == '10':
        ussd_trx.cancel_session()
        return
    
    response    = ussd_trx.get_response()
    status      = response['status']
    resp_msg    = response['msg']
    
    if status == 0 or status == 3: # success
        code = '2' # keep session open
    else:
        code = '3' # release session
        
    xml = '''
        <ussd>
            <type>'''+code+'''</type>
            <msg>'''+resp_msg+'''</msg> 
            <premium>
                <cost></cost>
                <ref></ref>
            </premium>
        </ussd>
        '''
    return HttpResponse(xml, content_type='application/xml')
    


def test_final_func(request):
    current_url = request.build_absolute_uri()
    print(current_url)
    return JsonResponse(1, safe=False)
    


@csrf_exempt
def halotel(request):
    if request.method == 'POST':
        # extract the SOAP XML from the POST data
        soap_xml = request.body.decode('utf-8')
        
        # parse the SOAP XML using ElementTree
        # root = ET.fromstring(soap_xml)
        soup    = BeautifulSoup(soap_xml, 'xml')
        root    = soup.find('InsertMO')
        
        passwd          = soup.find('pass').contents[0]  
        user            = root.user.contents[0]
        msisdn          = root.msisdn.contents[0]
        msg             = root.msg.contents[0]
        session_id      = root.transactionid.contents[0]
        requestType     = root.requestType.contents[0]
        ussdgw_id       = root.ussdgw_id.contents[0]
        
        
        code    = 0 # assume success
        # check if username and password is the same if not code = 1
        
        ussd_trx    = ussd_session(session_id,msisdn,msg)
        response    = ussd_trx.get_response()
        status      = response['status']
        resp_msg    = response['msg']
        
        
        # status 0 = success
        # status 2 = not valid shortcode
        # status 1 = system error
        # status 3 = last message
        # status 4 = expired session
        
        # check status
        if status == 0 or status == 3: # success
            code    = 0
            # send response via cellery
            if status == 0:
                req_type = '202'
            else:
                req_type = '203'
            
            print('sending req to cellery')
            send_response(resp_msg, session_id, req_type)
        
        elif status == 1: # system error
            code = -1
            
        elif status == 4: # expired session
            code = 2
        
        
        resp   = soap_response(code)
        return HttpResponse(resp, content_type='text/xml')
    else:
        return HttpResponseBadRequest('Invalid request method')  
     

def soap_response(code):
    
    xml     = '''
    <?xml version="1.0" encoding="utf-8"?>
    <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
        <soap:Body>
            <ussdresponse>
                    <errorCode>'''+str(code)+'''</errorCode>
            </ussdresponse>
        </soap:Body>
    </soap:Envelope>
    '''
    
    return xml