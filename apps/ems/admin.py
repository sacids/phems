from django.contrib import admin

from .models import *


class SignalAdmin(admin.ModelAdmin):
    list_display = ['id','channel','contents','relevance','status','created_on']
    
admin.site.register(Signal,SignalAdmin)


class SignalKeyAdmin(admin.ModelAdmin):
    list_display = ['keyword','weight']
    
admin.site.register(SignalKeys,SignalKeyAdmin)