from django.db import models
from django.db.models.deletion import CASCADE, PROTECT, DO_NOTHING
from django.contrib.auth.models import User

# Create your models here.
class Notification(models.Model):
    QN_OPTIONS = (
        ('PENDING', 'Pending'),
        ('SENT', 'Sent'),
        ('DELIVERED', 'Delivered'),
        ('REJECTED', 'Rejected'),    
    )

    message           = models.TextField()
    message_id        = models.CharField(max_length=50,blank=True, null=True)
    user              = models.ForeignKey(User, on_delete=models.CASCADE)
    email             = models.CharField(max_length=50,blank=True, null=True)
    phone             = models.CharField(max_length=20,blank=True, null=True)
    app_status        =  models.CharField(max_length=30, choices=QN_OPTIONS, default='PENDING') 
    email_status      =  models.CharField(max_length=30, choices=QN_OPTIONS, default='PENDING') 
    sms_status        =  models.CharField(max_length=30, choices=QN_OPTIONS, default='PENDING') 
    created_on        = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ph_notification'
        managed = True
        verbose_name = 'Notification'
        verbose_name_plural = 'Notification'