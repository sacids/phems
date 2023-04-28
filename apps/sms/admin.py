from django.contrib import admin

from .models import *


class SMSAdmin(admin.ModelAdmin):
    list_display = ['msg','msisdn','shortcode','smsc_id','created_on']
    
admin.site.register(SmsLog, SMSAdmin)