from django.shortcuts import render
from django.core.mail import EmailMessage
from django.core.mail import BadHeaderError
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from .models import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView 

from django.db.models import Q
import json

import random
import math
from django.contrib.auth.models import User

from django.views.decorators.csrf import csrf_exempt,csrf_protect


# sendEmail
def sendEmail(subject, message, fromEmail, toEmail):
    if subject and message:
        try:
            email = EmailMessage(
                subject,
                message,
                fromEmail,
                toEmail
            )
            email.content_subtype = "html"
            email.send(fail_silently=True)
            # response
            return JsonResponse({'error': False, 'message': 'Email sent'})
        except BadHeaderError:
            return JsonResponse({'error': True, 'message': 'Email failed'})
    else:
        return JsonResponse({'error': True, 'message': 'Email failed'})


def deleteMrvRowData(request):
    if request.method == 'POST':
        ids         = request.POST.get('ids')
        return JsonResponse(0,safe=False)
        del_ids     = ids.split(",")
        # delete ids
        if mrv_forms_data.objects.filter(pk__in=del_ids).update(deleted=True):
            return JsonResponse(1,safe=False)
        else:
            return JsonResponse(0,safe=False)
    else:
        return JsonResponse(0,safe=False)


@csrf_exempt
def activateUser(request):
    data        = json.loads(request.body.decode('utf-8'))
    otp         = data['otp']
    username    = data['username']

    cc = activation_otp.objects.filter(Q(user__username=username) and Q(otp=otp))

    if(cc.count()>0):
        # activate user
        user            = User.objects.get(username=username)
        user.is_active  = True
        user.save()
        context     = {}
        response    = HttpResponse(json.dumps(context), content_type='application/json')
        response.status_code = 200
    else:
        ret     = '{"status":0,"msg":"Account not activated"}'
        context     = {
            'status': 400,
            'detail': "Invalid code"
        }
        response    = HttpResponse(json.dumps(context), content_type='application/json')
        response.status_code = 400

    return response


@csrf_exempt
def registerUser(request):
    data = json.loads(request.body.decode('utf-8'))
    username        = data['username']
    last_name       = data['last_name']
    first_name      = data['first_name']
    password        = data['password']


    # check if username exists
    if(User.objects.filter(username=username).count() > 0):
        #user exists
        ret     = '{"status":1,"msg":"Username Exists"}'
        context     = {
            'status': 400,
            'detail': "Username Exists"
        }
        response    = HttpResponse(json.dumps(context), content_type='application/json')
        response.status_code = 400
    else:
        user = User.objects.create_user(
            username, 
            username, 
            password,
            first_name  = first_name,
            last_name   = last_name,
            is_active   = False
            )

        # create 6 digit OTP message
        otp     = create_otp(user)
        send_email(user,otp)

        ret     = '{"status":0,"msg":"User created successfully"}'

        context     = {}
        response    = HttpResponse(json.dumps(context), content_type='application/json')
        response.status_code = 200
    
    return response





def create_otp(user):
    digits = [i for i in range(0, 10)]
    random_str = ""
    for i in range(6):
        index = math.floor(random.random() * 10)
        random_str += str(digits[index])
    
    otp = activation_otp.objects.create(user=user,otp=random_str)
    return random_str

def send_email(user, otp):
    #current_site = get_current_site(request)
    subject = 'Activate Account'
    message = render_to_string('emails/account_activation_email_otp.html', {
        'user': user,
        'otp': otp,
    })
    user.email_user(subject, message)
    


class getMeView(APIView):
    http_method_names = ['get']
    permission_classes=[IsAuthenticated] 

    def get(self, request):
        response_data = {
            'result': 'Restricted access test ok.',
            'user': request.user.username,
        }
        return JsonResponse(response_data,safe=False)