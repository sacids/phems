import json
import os

import requests
from django.http import JsonResponse
from django.views import View
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from twilio.twiml.messaging_response import MessagingResponse

from apps.chatbot.models import Menu, MenuSession
from .utils import initMenu, nextMenu

TELEGRAM_URL = "https://api.telegram.org/bot"
BOT_TOKEN = "5210813918:AAEB0WKoRdQ8R3dMPVYXNmnS-4HwhtG8Ov4"

#whatsapp bot
@csrf_exempt
def whatsapp(request):
    user = request.POST.get('From')
    message = request.POST.get('Body')
    print(f'{user} says {message}')

    #substring phone
    phone = user[-12:]

    #todo: check menu session if active=0
    menu_session = MenuSession.objects.filter(phone=phone, active=0)

    if menu_session.count() > 0:
        #get latest menu session
        m_session = MenuSession.objects.filter(phone=phone, active=0).latest('id')

        #check for menu flag
        menu = Menu.objects.get(pk =m_session.menu_id)

        if(menu.flag == 'Tukio_Ending'):
            result = initMenu('whatsapp', phone)
            data = json.loads(result.content) 
        else:    
            result = nextMenu('whatsapp', phone , m_session.menu_id, message)
            data = json.loads(result.content)

        #response
        response = MessagingResponse()
        response.message(data['message'])

    else:
        result = initMenu('whatsapp', phone)
        data = json.loads(result.content)

        #response
        response = MessagingResponse()
        response.message(data['message'])

    return HttpResponse(str(response))


#telegram bot
@csrf_exempt
def telegram(request):
    t_data = json.loads(request.body)
    t_message = t_data["message"]
    t_chat = t_message["chat"]

    

    print(f'telegram bot says {t_message}')

    msg = "Thank for your message! Sacids Team will be back to you shortly!"
    send_message(msg, t_chat["id"])

    return JsonResponse({"ok": "POST request processed"})

# @staticmethod
def send_message(message, chat_id):
    data = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown",
    }
    response = requests.post(
            f"{TELEGRAM_URL}{BOT_TOKEN}/sendMessage", data=data
        )