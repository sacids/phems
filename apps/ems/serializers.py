from rest_framework import serializers
from .models import *


class SignalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Signal # this is the model that is being serialized
        fields = ('channel','contents','contact','status','created_on')
        read_only_fields =  ('created_on','status')
        
        

class KeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = SignalKeys # this is the model that is being serialized
        fields = ('keyword','weight')




