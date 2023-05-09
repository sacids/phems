from celery import shared_task
from django.http import JsonResponse, HttpResponse
import requests

import config.mno_config as cfg


@shared_task
def send_sms(msisdn, shortcode, smsc, msg):
    
    
    pass