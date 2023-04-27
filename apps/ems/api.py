from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import *
from .models import *

# Create your views here.
#/api/ems/signals/
class SignalViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows signals to be viewed or edited.
    """
    queryset = Signal.objects.all().order_by('-created_on')
    serializer_class = SignalSerializer
    #permission_classes = [permissions.IsAuthenticated]
    
    

class KeywordViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Keywords to be viewed or edited.
    """
    queryset = SignalKeys.objects.all()
    serializer_class = KeywordSerializer
    #permission_classes = [permissions.IsAuthenticated]