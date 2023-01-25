from dataclasses import fields
from rest_framework import serializers
from apps.ems.models import *

class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Event    