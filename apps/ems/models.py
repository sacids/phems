from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import json
from .utils import calc_relevance
from treebeard.mp_tree import MP_Node

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models.deletion import CASCADE, PROTECT, DO_NOTHING
from django.contrib.postgres.fields import JSONField
from django.urls import reverse
from django.utils.datetime_safe import date
from django.contrib.auth.models import Group
from django.contrib.contenttypes.fields import GenericRelation
from jellyfish import soundex, metaphone
import os



# Create your models here.
class Signal(models.Model):
    
    CHANNEL = (
        ('SMS', 'SMS'),
        ('WHATSAPP', 'WhatsApp'),
        ('TELEGRAM', 'Telegram'),
        ('TWITTER', 'Twitter'),
        ('WEB', 'Web'),
        ('APP', 'App'),
    )
    
    STATUS  = (
        ('NEW', 'New'),
        ('ADDED', 'Added'),
        ('DISCARDED', 'Discarded'),
    )
    
    channel         = models.CharField(max_length=15,choices=CHANNEL,default='WEB')
    contact         = models.CharField(max_length=50,blank=True, null=True)
    contents        = models.JSONField(null=False)
    relevance       = models.IntegerField(default=0)
    status          = models.CharField(max_length=14,choices=STATUS,default='NEW')
    created_on      = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table    = 'ph_signal'
        
    def __str__(self):
        return self.channel if self.channel else self.pk

    @property
    def css_icon(self):
        if self.channel == 'SMS':
            return 'bx bx-message-alt-dots text-primary '
        if self.channel == 'WHATSAPP':
            return 'bx bxl-whatsapp text-success '
        if self.channel == 'TELEGRAM':
            return 'bx bxl-telegram text-info '
        if self.channel == 'TWITTER':
            return 'bx bxl-twitter text-info '
        if self.channel == 'WEB':
            return 'bx bxl-html5 text-warning '
        if self.channel == 'APP':
            return 'bx bxl-android text-danger '
     
     
    def save(self, *args, **kwargs):
        with open("assets/json/keywords.json", 'r') as file:
            key_map = json.loads(file.read().rstrip())
        self.relevance = calc_relevance(str(self.contents),key_map)
        super(Signal, self).save(*args, **kwargs)





class Sector(models.Model):

    title           = models.CharField(max_length=50)


    def __str__(self):
        return self.title

    class Meta:
        db_table = 'ph_sector'
        managed = True
        verbose_name = 'Sector'
        verbose_name_plural = 'Sectors'    

class Contact(models.Model):

    CONTACT_SOURCE  = (
        ('ORIGINAL', 'Original'),
        ('SECOND_HAND', 'Second-Hand')
    )

    CONTACT_TYPE = {
        ('PHONE','Phone Number'),
        ('ADDRESS','Address'),
        ('EMAIL','E-mail'),
    }

    full_name       = models.CharField(max_length = 150)
    contact_source  = models.CharField(max_length=15,choices=CONTACT_SOURCE,default='SECOND_HAND')
    #contact_type    = models.CharField(max_length=15,choices=CONTACT_TYPE,default='PHONE')
    contact_data    = models.CharField(max_length = 150)
    
    def __str__(self):
        return self.full_name

    class Meta:
        db_table = 'ph_contact'
        managed = True
        verbose_name = 'contact'
        verbose_name_plural = 'contacts'

class Stage(models.Model):
    
    title           = models.CharField(max_length=255)
    form            = models.ForeignKey('Form', on_delete=models.CASCADE,blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'ph_stage'
        verbose_name_plural = 'Stages'

    pass


class Location(MP_Node):

    title           = models.CharField(max_length = 200)
    code            = models.CharField(max_length=10, blank=True, null=True)
    p_id            = models.CharField(max_length = 25)
    
    
    def __str__(self):
        return self.title

    class Meta:
        db_table = 'ph_location'
        managed = True
        verbose_name = 'Location'
        verbose_name_plural = 'Locations'


class Event(models.Model):
  
    STATUS  = (
        ('NEW', 'New'),
        ('DISCARED', 'Discarded'),
        ('PROGRESS', 'On Progress'),
        ('COMPLETE', 'Complete'),
    )
    
    PROFESSION = (
        ('CHW', 'Community Health Worker'),
        ('LFO', 'Livestock Field Officer'),
        ('HW', 'Health Worker'),
    )

    title           = models.CharField(max_length=150,blank=True, null=True)
    description     = models.TextField(blank=True, null=True)
    signal          = models.ManyToManyField("Signal")
    status          = models.CharField(max_length=14,choices=STATUS,default='NEW')
    stage           = models.ForeignKey('stage', on_delete=DO_NOTHING,default=1) 
    location        = models.ForeignKey('location', on_delete=DO_NOTHING) 
    sector          = models.ManyToManyField(Sector)
    
    contact_name    = models.CharField(max_length=150, blank=True, null=True)
    contact_prof    = models.CharField(max_length=20,choices=PROFESSION,default='HW')
    contact_phone   = models.CharField(max_length=20, blank=True, null=True)
    contact_email   = models.CharField(max_length=50,blank=True, null=True)
    
    created_on      = models.DateTimeField(auto_now=True)

    notes           = GenericRelation('note')    
    files           = GenericRelation('files')   
    user_access     = GenericRelation('perms_user')  
    group_access    = GenericRelation('perms_group')   
      

    def __str__(self):
        return self.description

    class Meta:
        db_table = 'ph_event'
        managed = True
        verbose_name = 'Event'
        verbose_name_plural = 'Events'
    

             
class SignalKeys(models.Model):

    keyword         = models.CharField(max_length=50)
    weight          = models.SmallIntegerField(default=1)
    sector          = models.ForeignKey(Sector, on_delete=models.CASCADE, blank=True, null=True)
    
    class Meta:
        db_table    = 'ph_signal_keys'
        verbose_name_plural = 'SignalKeys'
        
    def __str__(self):
        return self.keyword if self.keyword else str(self.pk)
    
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
        return os.path.basename(self.obj.name)

    @property
    def css_icon(self):
        name, extension = os.path.splitext(self.obj.name)
        if extension == '.pdf':
            return 'mdi mdi-file-pdf text-red-500 '
        if extension == '.docx':
            return 'mdi mdi-file-document text-blue-500 '
        if extension == '.txt':
            return 'mdi mdi-text-box'
        if extension == '.jpeg':
            return 'mdi mdi-image text-emerald-500 '
        if extension == '.xlsx':
            return 'mdi mdi-file-excel-box text-emerald-500 '
        
        return 'mdi mdi-file text-emerald-500 '

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
        
        
class workflow_config(models.Model):
    label           = models.CharField(max_length=50,blank=True, null=True) 
    cur_stage       = models.ForeignKey('Stage', related_name='cur_stage', on_delete=models.CASCADE)
    next_stage      = models.ForeignKey('Stage', related_name='next_stage', on_delete=models.CASCADE)
    
    

    def __str__(self):
        return self.cur_stage.title+' - '+self.next_stage.title

    class Meta:
        db_table = 'ph_workflow_cfg'
        verbose_name_plural = 'Workflow Config'
        
        
class workflow_data(models.Model):
    event           = models.ForeignKey('Event', on_delete=models.CASCADE)
    stage           = models.ForeignKey('Stage', related_name='workflow_stage', on_delete=models.CASCADE)
    data            = models.JSONField(null=False)
    created_at      = models.DateTimeField(auto_now_add=True, null=True)
    created_by      = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=PROTECT)
      
    def __str__(self):
        return 'WF: '+self.event.title

    class Meta:
        db_table = 'ph_workflow_data'
        verbose_name_plural = 'Workflow Data'
        
        
        
class Form(models.Model):
    title       = models.CharField(max_length=50)
    description = models.TextField()
    created_on  = models.DateTimeField(auto_now=True)
    created_by  = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'ph_forms'
        managed = True

    def __str__(self):
        return self.title if self.title else self.pk

class Form_config(models.Model):

    QN_OPTIONS = (
        ('DATE', 'Date'),
        ('BARCODE', 'Barcode'),
        ('INT', 'Numeric'),
        ('GEOPOINT', 'Geopoint'),
        ('TEXT', 'String'),
        ('INT', 'int'),
        ('SELECT1', 'Select1'),
        ('SELECT', 'Select'),
        ('BINARY', 'Binary'),
        ('TIME', 'Time'),
        ('DATETIME', 'DateTime'),
    )

    form        = models.ForeignKey('Form', on_delete=models.CASCADE)
    ref         = models.CharField(max_length=100,blank=True, null=True)
    col_name    = models.CharField(max_length=50)
    col_type    = models.CharField(max_length=10,choices=QN_OPTIONS,default='TEXT')
    options     = models.TextField(null=True,blank=True)
    hint        = models.TextField(null=True,blank=True)
    label       = models.TextField(null=True,blank=True)
    constraints = models.TextField(blank=True, null=True)
    required    = models.CharField(max_length=1,default=0)
    order       = models.IntegerField(blank=True, null=True,default=0)
    page        = models.IntegerField(blank=True, null=True,default=0)

    class Meta:
        db_table = 'ph_forms_cfgf'
        managed = True
