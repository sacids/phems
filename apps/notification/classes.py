import random
import string
import json
import requests
from datetime import datetime
from django.http import JsonResponse
from django.contrib.auth.models import User, Group
from .models import Notification


class NotificationWrapper:
    BASE_URL   = "http://127.0.0.1:8000/"
    API_TOKEN  = "" #for sending sms

    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {self.API_TOKEN}",
            "Content-Type": "application/json",
        }
        self.API_URL = self.BASE_URL


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
