from django.shortcuts import render
import json
import zeep
import requests
from django.db.models import Q
from .models import *
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
import config.mno_config as cfg


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
        new_sms.to_string()
        # new_sms.process() 
        
        resp   = soap_response(0)
        return HttpResponse(resp, content_type='text/xml')
    

def smpp_rec(request):
    
    msg         = request.GET['msg']
    msisdn      = request.GET['msisdn']
    shortcode   = request.GET['shortcode']
    smsc_id     = request.GET['smsc_id']
    
    
    SmsLog.objects.create(msisdn=msisdn,shortcode=shortcode,smsc_id=smsc_id,msg=msg)
    return JsonResponse(1,safe=False)

def send_sms(request):
    pass



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
        
    def to_string(self):
        print(self.mno,' : ',str(self.shortcode),' : ',str(self.msisdn),' : ',self.msg)
        
    def process(self):
        pass
    
    def send_sms(self):
        if self.mno     == 'halotel':
            self._smpp_send()
        else:
            self._kannel_send()
            
    
    
    def _kannel_send(self):
        url         = cfg.kannel['send_sms_url']+'?user='+cfg.kannel['send_sms_username']+'&pass='+cfg.kannel['send_sms_passwd']+'&text='+self.msg+'to='+self.msisdn+'&from='+self.shortcode+'smsc='+self.mno
        ret         = requests.get(url)
        return ret.json()
       
    
    def _smpp_send(self):
        wsdl        = cfg.halotel['send_sms_wsdl']
        client      = zeep.Client(wsdl=wsdl)
        response    = client.service.smsRequest(cfg.halotel['username'], cfg.halotel['password'], self.msisdn, self.msg, self.shortcode)
        return response
    
    