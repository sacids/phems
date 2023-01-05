from apps.ems.models import *
from .serializers import AlertSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime

# Create your views here.
class AlertList(APIView):
    """API to fetch alerts"""
    def get(self, request, format=None):
        alerts = Event.objects.all().order_by('-created_on')

        arr_data = []
        for alert in alerts:
            #create dict
            chart = {
                'id': alert.id,
                'title': alert.title,
                'description': alert.description,
                'status': alert.status,
                'created_on': date.strftime(alert.created_on, '%d/%m/%Y %H:%M'),
                'location': alert.location.title,
                'stage': alert.stage.title,
                'alert_type': alert.alert.title,
                'primary_sector': alert.pri_sector.title
            } 
            #append to arr_data
            arr_data.append(chart)

        return Response(arr_data, status = status.HTTP_200_OK)


    def post(self, request, format=None):
        serializer = AlertSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST) 



class RumorList(APIView):
    """API to fetch rumors""" 
    def get(self, request, format=None):
        rumors = Signal.objects.filter(status="NEW").order_by('-created_on','-relevance')

        arr_data = []
        for rumor in rumors:
            #create dict
            chart = {
                'id': rumor.id,
                'title': rumor.contents['text'],
                'channel': rumor.channel,
                'status': rumor.status,
                'created_on': date.strftime(rumor.created_on, '%d/%m/%Y %H:%M'),
                'relevance': rumor.relevance,
                'contact': rumor.contact,
            } 
            #append to arr_data
            arr_data.append(chart)

        return Response(arr_data, status = status.HTTP_200_OK)


    def post(self, request, format=None):
        serializer = AlertSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)       
