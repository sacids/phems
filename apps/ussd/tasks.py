from celery import shared_task
from django.http import JsonResponse, HttpResponse

USERNAME    = ''
PASSWORD    = ''

@shared_task
def send_response(msg, session_id, req_type):
    xml   = '''
    <?xml version="1.0" encoding="utf-8"?>
    <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"xmlns:xsi="htt p://www.w3.org/2001/XMLSchema- instance"xmlns:xsd="http://www.w3.org/2001/XMLSchema">
        <soap:Body>
            <InsertMO xmlns="http://tempuri.org/">
                <user>'''+USERNAME+'''</user>
                <pass>'''+PASSWORD+'''</pass>
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
    
    print(xml)
    ### post xml