from django.shortcuts import render
import json
import zeep
from zeep import Settings
import requests
from django.db.models import Q
from .models import *
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
import config.mno_config as cfg
import logging
import base64

from .tasks import send_sms


## halotel
from django.views.decorators.csrf import csrf_exempt
from bs4 import BeautifulSoup

@csrf_exempt
def soap_rec(request):
    if request.method == 'POST':
        # extract the SOAP XML from the POST data
        soap_xml    = request.body.decode('utf-8')
        
        soup        = BeautifulSoup(soap_xml, 'xml')
        root        = soup.find('moRequest')
        
        msisdn      = root.source.contents[0]
        shortcode   = root.dest.contents[0]
        msg         = root.content.contents[0]
        username    = root.username.contents[0]
        password    = root.password.contents[0]
    
        new_sms     = sms('halotel',shortcode,msisdn,msg)
        new_sms.process()
        # new_sms.process() 
        
        resp   = soap_response(0)
        return HttpResponse(resp, content_type='text/xml')
    

def smpp_rec(request):
    
    msg         = request.GET['msg']
    msisdn      = request.GET['msisdn']
    shortcode   = request.GET['shortcode']
    smsc_id     = request.GET['smsc_id']
    
    new_sms     = sms(smsc_id,shortcode,msisdn,msg)
    new_sms.process()
    
    return JsonResponse(1,safe=False)


def is_authorized_sender(request):
    
    source_ip = request.META.get('REMOTE_ADDR')
    local_ips = ['127.0.0.1','172.16.16.20']  # Add your local network IP ranges if needed

    # Check if the source IP matches the local IPs
    if source_ip not in local_ips:
        return 0
    
    Auth                = request.headers.get('Authorization')
    credentials         = f"{cfg.ems['send_sms_user']}:{cfg.ems['send_sms_passwd']}"
    if base64.b64encode(credentials.encode('utf-8')).decode('utf-8') != Auth.split()[1]:
        return 0

    return 1



@csrf_exempt
def send_sms(request):
    
    if request.method == 'POST':
        
        if not is_authorized_sender(request):
            logging.info('Un-authorized SMS sender')
            return HttpResponse("Access Denied", status=403)
  
        smsc        = request.POST.get('mno',0)
        msisdn      = request.POST.get('to',0)
        msg         = request.POST.get('msg',0)
        shortcode   = request.POST.get('from',0)
        
        response    = {'status': 1, 'msg': 'Accepted for delivery'}
        #if sender not set default to 190
        if smsc or msisdn or msg or shortcode:
            response['status']  = 0
            response['msg']     = 'Invalid Parameters'
        else:
            oSms =  sms(smsc,shortcode,msisdn,msg)
            response = oSms.send()
            
        return JsonResponse(response,safe=False)



def submit_rumor():
    pass


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


class sms: 
    
    def __init__(self,mno,shortcode,msisdn,msg):
        self.shortcode  = shortcode
        self.msisdn     = msisdn
        self.msg        = msg
        self.mno        = mno
         
        # log sms 
        logging.info(self.to_string)
        SmsLog.objects.create(msisdn=msisdn,shortcode=shortcode,smsc_id=mno,msg=msg)
        
    def to_string(self):
        return 'NEW SMS : '+self.mno+' : '+str(self.shortcode)+' : '+str(self.msisdn)+' : '+self.msg
        
    def process(self):
        
        payload =   {
            'channel':  'SMS',
            'contact':  self.msisdn,
            'contents': '{"text":"'+self.msg+'"}',
        }
        response = requests.request("POST", cfg.ems['signal_post_url'], data=payload)
        logging.info(response.text)

    
    def send(self):
        if self.mno     == 'halotel':
            self._soap_send()
        else:
            self._kannel_send()

    
    def _kannel_send(self):
        url         = cfg.kannel['send_sms_url']+'?user='+cfg.kannel['send_sms_username']+'&pass='+cfg.kannel['send_sms_passwd']+'&text='+self.msg+'to='+self.msisdn+'&from='+self.shortcode+'smsc='+self.mno
        ret         = requests.get(url)
        logging.info('SENDING SMS : '+self.mno+' : '+ret.json())
        return ret.json()
       
    
    def _soap_send(self):
        wsdl        = cfg.halotel['send_sms_wsdl']
        settings    = Settings(strict=False, xml_huge_tree=True)
        client      = zeep.Client(wsdl=wsdl,settings=settings)
        response    = client.service.smsRequest(cfg.halotel['username'], cfg.halotel['password'], self.msisdn, self.msg, self.shortcode)
        logging.info('SENDING SMS : HALOTEL : '+response)
        return response
    
    