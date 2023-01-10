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


class ReportsList(APIView):
    """API to fetch situation reports""" 
    def get(self, request, format=None):
        arr_data = []

        #create dict
        chart = {
            'id': 1,
            'title': 'The Situation Report (SITREP) on floods in Moshi district',
            'sitrep_no': '69/ 2021',
            'date_issue': '03 April 2021',
            'region': 'Kilimanjaro',
            'district': 'Moshi',
            'ward': '',
            'village': 'Mandaka Mnono, Kudia na Korini',
            'date_occured': '15-23 April, 2021',
            'time_occured': 'AM',
            'source_of_event': 'The floods in Moshi District were caused by heavy rains up to three rivers (RAU, Manguvu and Kisangiro overflowing into residential areas.',
            'general_impact': 'One (1) person died, 2 people were wounded, 164 were affected, 30 houses were damaged and 2 were destroyed, 14 km of roads were damaged, 2 bridges were damaged, and 1,100 acres were destroyed.',
            'created_on': '03 April, 2021',
        } 
        #append to arr_data
        arr_data.append(chart)

        return Response(arr_data, status = status.HTTP_200_OK)