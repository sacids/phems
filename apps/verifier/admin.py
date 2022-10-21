from django.contrib import admin
from .models import *

# Register your models here.
class VerifierAdmin(admin.ModelAdmin):
    list_display = ['id','user', 'credibility_score' ,'created_on']
    
admin.site.register(Verifier,VerifierAdmin)
