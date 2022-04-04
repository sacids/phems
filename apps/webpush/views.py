from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt,csrf_protect

from rest_framework_simplejwt.backends import TokenBackend
from rest_framework.permissions import IsAuthenticated

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User
from apps.account.models import Profile
from pywebpush import webpush, WebPushException



# Create your views here.






VAPID_PRIVATE_KEY   = 'Ccj5wQZeIinwRyinMcWmFV8oyuiYUmFGCiqKHYdxjyY'
VAPID_PUBLIC_KEY    = 'BKuw1Bv-N6O3atv3-ZQ1PERHewSy5nviEfE-sFxmIHdfiOZwsRzMJ76JU3fN-lO4m8Pz1eBidTVhQoFXnJl_Grs'




@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def subscription(request):
    if request.method == 'GET':
        response                                = HttpResponse(json.dumps('{"public_key":"'+VAPID_PUBLIC_KEY+'"}'))
        response['Access-Control-Allow-Origin'] = '*'
        response['content_type']                = 'application/json'
        return response
    else:
        print(request.user.username)
        p = Profile.objects.get(user=request.user)
        sub_token   = request.POST.get('subscription_token')
        print(sub_token)
        p.sub_token     = sub_token
        p.save()
        print(p.sub_token)
        return HttpResponse(p.sub_token)
    
def send_push(request):
    p = Profile.objects.get(user__username='admin@admin.com')
    sub_token   = json.loads(p.sub_token)
    data        = 'This is my sample data natesti mara mia'
    
    try:
        webpush(
            subscription_info=sub_token,
            data=data,
            vapid_private_key=VAPID_PRIVATE_KEY,
            vapid_claims={"sub": "mailto:ericbeda@gmail.com"})
        return HttpResponse(1)
    except WebPushException as ex:
        print("I'm sorry, Dave, but I can't do that: {}", repr(ex))
        # Mozilla returns additional information in the body of the response.
        if ex.response and ex.response.json():
            extra = ex.response.json()
            print("Remote service replied with a {}:{}, {}",
                extra.code,
                extra.errno,
                extra.message
                )
        return HttpResponse(0)
    