import json
import os

import requests
from django.http import JsonResponse
from django.views import View
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from twilio.twiml.messaging_response import MessagingResponse

TELEGRAM_URL = "https://api.telegram.org/bot"
BOT_TOKEN = "5210813918:AAEB0WKoRdQ8R3dMPVYXNmnS-4HwhtG8Ov4"


@csrf_exempt
def message(request):
    user = request.POST.get('From')
    message = request.POST.get('Body')
    print(f'{user} says {message}')

    response = MessagingResponse()
    response.message('Thank for your message! Sacids Team will be back to you shortly!')
    return HttpResponse(str(response))


#telegram bot
def telbot(self, request):
    t_data = json.loads(request.body)
    t_message = t_data["message"]
    t_chat = t_message["chat"]

    print(f'telegram bot says {t_message}')

    msg = "Thank for your message! Sacids Team will be back to you shortly!"
    # self.send_message(msg, t_chat["id"])

    return JsonResponse({"ok": "POST request processed"})

# @staticmethod
# def send_message(message, chat_id):
#     data = {
#         "chat_id": chat_id,
#         "text": message,
#         "parse_mode": "Markdown",
#     }
#     response = requests.post(
#             f"{TELEGRAM_URL}{TUTORIAL_BOT_TOKEN}/sendMessage", data=data
#         )