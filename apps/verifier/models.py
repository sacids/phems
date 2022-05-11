from django.db import models
from django.db.models.deletion import CASCADE, PROTECT, DO_NOTHING
from apps.ems.models import *

# Create your models here.
class Verifier(models.Model):
    user              = models.OneToOneField(User, on_delete=models.CASCADE, default=1)
    location          =  models.ForeignKey(Location, on_delete=DO_NOTHING) 
    credibility_score =  models.FloatField(null=True, blank=True, default=0)
    created_on   = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ph_verifiers'
        managed = True
        verbose_name = 'Verifier'
        verbose_name_plural = 'Verifiers'

