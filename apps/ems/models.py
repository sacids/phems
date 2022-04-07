from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import json
from .utils import *
from jellyfish import soundex, metaphone



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
    relevance       = models.IntegerField(default=0)
    status          = models.CharField(max_length=14,choices=STATUS,default='NEW')
    created_on      = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table    = 'ph_signal'
        
    def __str__(self):
        return self.channel if self.channel else self.pk
     
     
    def save(self, *args, **kwargs):
        with open("assets/json/keywords.json", 'r') as file:
            key_map = json.loads(file.read().rstrip())
        self.relevance = calc_relevance(str(self.contents),key_map)
        super(Signal, self).save(*args, **kwargs)
            
            
            
                   
class SignalKeys(models.Model):

    keyword         = models.CharField(max_length=50)
    weight          = models.SmallIntegerField(default=1)
    
    class Meta:
        db_table    = 'ph_signal_keys'
        
    def __str__(self):
        return self.keyword if self.keyword else self.pk
    
    @receiver(post_save, sender='ems.SignalKeys')
    def update_keyword_json(sender, instance, created, **kwargs):
        keywords    = SignalKeys.objects.all()
        tt  = {}
        for item in keywords:
            tt[soundex(item.keyword)] = item.weight
        with open("assets/json/keywords.json", "w") as file_object:
            json.dump(tt,file_object)
        
        
    
        