from django.contrib import admin
from .models import *

# Register your models here.
class VerifierAdmin(admin.ModelAdmin):
    list_display = ['id','full_name', 'credit_score' ,'active','created_on']
    
admin.site.register(Verifier,VerifierAdmin)
