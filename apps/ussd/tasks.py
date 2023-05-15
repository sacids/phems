from celery import shared_task
from django.http import JsonResponse, HttpResponse
import requests

import config.mno_config as cfg
import logging


@shared_task
def send_response(msg, session_id, req_type):
    xml   = '''
    <?xml version="1.0" encoding="utf-8"?>
    <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
        <soap:Body>
            <InsertMO xmlns="http://tempuri.org/">
                <user>'''+cfg.halotel['hal_ussd_user']+'''</user>
                <pass>'''+cfg.halotel['hal_ussd_pass']+'''</pass>
                <msisdn>null</msisdn>
                <msg>'''+msg+'''</msg>
                <sessionid>null</sessionid> 
                <transactionid>'''+session_id+'''</transactionid> 
                <requestType>'''+req_type+'''</requestType> 
                <ussdgw_id>1</ussdgw_id>
            </InsertMO>
        </soap:Body>
    </soap:Envelope>
    '''
    
    ### post xml
    logging.info('send req in cellery '+xml)
    
    ret         = requests.post(cfg.halotel['send_ussd_url'],data=xml)
    logging.info(ret.text)
    return ret