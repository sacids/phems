from rest_framework import serializers
from .models import *


class SignalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Signal # this is the model that is being serialized
        fields = ('channel','contents','status','created_on')
        read_only_fields =  ('created_on','status')




