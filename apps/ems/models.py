from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Signal(models.Model):
    
    CHANNEL = (
        ('SMS', 'SMS'),
        ('CHATBOT', 'ChatBot'),
        ('WEB', 'Web'),
        ('APP', 'App'),
    )
    
    STATUS  = (
        ('NEW', 'New'),
        ('ADDED', 'Added'),
        ('DISCARDED', 'Discarded'),
    )
    
    channel         = models.CharField(max_length=15,choices=CHANNEL,default='WEB')
    contents        = models.JSONField(null=False)
    status          = models.CharField(max_length=14,choices=STATUS,default='NEW')
    created_on      = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table    = 'ph_signal'
        managed     = True
