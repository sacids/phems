import random
import string
import json
import requests
from datetime import datetime
from django.http import JsonResponse
from django.contrib.auth.models import User, Group
from .models import Notification
from decouple import config

import urllib3
urllib3.disable_warnings()


class NotificationWrapper:
    API_BASE_URL = 'https://apisms.beem.africa/v1/send'
    API_DELIVERY_URL = 'https://dlrapi.beem.africa/public/v1/delivery-reports'

    api_key = config('API_KEY')
    secret_key = config('SECRET_KEY')

    def __init__(self):
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": "Basic " + self.api_key + ":" + self.secret_key,
        }


    def create_notification(self, **kwargs):
        """ Create notification for different users """
        message        = kwargs['message']
        url            = kwargs['url']
        user_id        = kwargs['user_id']
        created_by     = kwargs['created_by']

        """random code"""
        message_id = ''.join(random.choices(string.ascii_uppercase, k=12))

        """query for user"""
        user = User.objects.filter(pk=user_id) 

        if user.count() > 0:
            """user"""
            user = user.first()
            
            """new notification"""
            new_data = Notification()
            new_data.message = message
            new_data.url = url
            new_data.message_id = message_id
            new_data.email = user.email
            new_data.user_id = user.pk
            new_data.created_by_id =  created_by
            new_data.save()

            """return response"""
            return JsonResponse({'error': False, 'message': 'Notification created'})
        else:
            return JsonResponse({'error': True, 'message': 'User does not exist!'}) 


    def send_sms(self, arr_data):
        """send sms"""
        request = requests.post(url = self.API_BASE_URL, data = json.dumps(arr_data),
                                headers=self.headers,
        auth=(self.api_key, self.secret_key),verify=False)

        print(request.status_code)
        print(request.json())

        """return response"""
        return JsonResponse(request.json())
    

    def delivery_report(self, arr_data):
        """get delivery report"""
        payload = {
            'headers': self.headers,
            'params': arr_data
        }

        print(payload)

        request = requests.get(url=self.API_DELIVERY_URL, data=json.dumps(payload), 
                                auth=(self.api_key, self.secret_key), verify=False)
        print(request.json())

        """return response"""
        return JsonResponse(request.json())

    
    def cast_phone_number(self, **kwargs):
        """cast phone number"""
        phone = str(kwargs['phone'])

        if phone.startswith('0'):
            return "255" + phone[1:]
        elif len(phone) == 9:
            return "255" + phone
        else:
            return phone