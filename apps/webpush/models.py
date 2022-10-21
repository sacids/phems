
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class AccessToken(models.Model):
    user            = models.OneToOneField(User, on_delete=models.CASCADE)
    sub_token       = models.TextField(blank=True, null=True)
    
    class Meta:
        db_table    = 'ph_token'
        managed     = True