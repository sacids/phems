from django.db import models
from django.db.models.deletion import CASCADE, PROTECT, DO_NOTHING
from apps.ems.models import *

# Create your models here.
class Verifier(models.Model):
    full_name    =  models.CharField(max_length = 150)
    location     =  models.ForeignKey(Location, on_delete=DO_NOTHING) 
    sector       =  models.ManyToManyField(Sector)
    credit_score =  models.FloatField(null=True, blank=True)
    active       =  models.IntegerField(default=0)
    created_on   = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name

    class Meta:
        db_table = 'ph_verifiers'
        managed = True
        verbose_name = 'Verifier'
        verbose_name_plural = 'Verifiers'

