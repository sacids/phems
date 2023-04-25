from django.db import models

# Create your models here.

class SmsLog(models.Model):
    
    msg             = models.CharField(max_length=250)
    smsc_id         = models.CharField(max_length=50)
    shortcode       = models.CharField(max_length=50)
    msisdn          = models.CharField(max_length=50)
    created_on      = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.msg

    class Meta:
        db_table = 'sms_incoming'
        managed = True
        verbose_name = 'Incoming SMS'
        verbose_name_plural = 'Incoming SMS'