from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import json
from .utils import *

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models.deletion import CASCADE, PROTECT, DO_NOTHING
from django.contrib.postgres.fields import JSONField
from django.urls import reverse
from django.utils.datetime_safe import date
from django.contrib.auth.models import Group
from django.contrib.contenttypes.fields import GenericRelation
import os



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
    contact         = models.CharField(max_length=50)
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





class Sector(models.Model):

    title           = models.CharField(max_length=50)


    def __str__(self):
        pass

    class Meta:
        db_table = 'ph_sector'
        managed = True
        verbose_name = 'Sector'
        verbose_name_plural = 'Sectors'    



class Event(models.Model):
  
    STATUS  = (
        ('NEW', 'New'),
        ('CONFIRMED', 'Confirmed'),
        ('ASSESSMENT', 'Risk Assessment'),
        ('VERIFIED', 'Verified'),
        ('DISCAREDED', 'Discarded'),
        ('PROGRESS', 'Response in Progress'),
        ('COMPLETED', 'Completed'),
    )


    signal          = models.ManyToManyField("Signal")
    status          = models.CharField(max_length=14,choices=STATUS,default='NEW')
    location        = models.IntegerField(default=0)
    sector          = models.ManyToManyField(Sector)



    notes           = GenericRelation('note')    
    files           = GenericRelation('files')   
    user_access     = GenericRelation('perms_user')  
    group_access    = GenericRelation('perms_group')   
      

    def __str__(self):
        pass

    class Meta:
        db_table = 'ph_event'
        managed = True
        verbose_name = 'Event'
        verbose_name_plural = 'Events'
    
                   
class SignalKeys(models.Model):

    keyword         = models.CharField(max_length=50)
    weight          = models.SmallIntegerField(default=1)
    sector          = models.ForeignKey(Sector, on_delete=models.CASCADE)
    
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
        
        
    
class files(models.Model):

    title       = models.CharField(max_length=50) 
    obj         = models.FileField(upload_to='assets/library', max_length=100)
    created_at  = models.DateTimeField(auto_now_add=True, null=True)
    created_by  = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=PROTECT)

    # Below the mandatory fields for generic relation
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id    = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    def __str__(self):
        return str(self.id)
    
    @property
    def filename(self):
        return os.path.basename(self.doc.name)

    @property
    def css_icon(self):
        name, extension = os.path.splitext(self.doc.name)
        print(extension)
        if extension == '.pdf':
            return 'mdi mdi-file-pdf text-danger '
        if extension == '.docx':
            return 'mdi mdi-file-document text-primary '
        if extension == '.txt':
            return 'mdi mdi-text-box'
        if extension == '.jpeg':
            return 'mdi mdi-image text-success '
        if extension == '.xlsx':
            return 'mdi mdi-file-excel-box text-success '
        
        return 'mdi mdi-file text-success '

    class Meta:
        db_table = 'ph_files'
        managed = True
        verbose_name = 'File'
        verbose_name_plural = 'Files'


class perms_group(models.Model):

    group        = models.ForeignKey(Group, on_delete=CASCADE) 

    # Below the mandatory fields for generic relation
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id    = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    def __str__(self):
        return self.group.name

    class Meta:
        db_table = 'ph_perms_group'
        verbose_name_plural = 'Group Perms'


class perms_user(models.Model):

    user        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE) 

    # Below the mandatory fields for generic relation
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id    = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    def __str__(self):
        return self.user.username

    class Meta:
        db_table = 'ph_perms_users'
        verbose_name_plural = 'User Perms'



class note(models.Model):
    message     = models.TextField(blank=True, null=True)
    created_at  = models.DateTimeField(auto_now_add=True, null=True)
    created_by  = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=PROTECT)  

    # Below the mandatory fields for generic relation
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()


    class Meta:
        db_table = 'ph_notes'
        verbose_name_plural = 'Notes'