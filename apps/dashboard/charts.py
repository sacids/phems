import json
from operator import ne
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.db.models import Sum, Count
from apps.ems.models import Signal, Event, Sector

class SignalPercentageChartView(APIView):
    def get(self, request, format=None):
        # signals
        signals = Signal.objects

        # discarded signals
        discarded = signals.filter(status='DISCARDED').count()

        # success signals
        success = signals.filter(status='ADDED').count()

        # aggregate
        aggregate = discarded + success

        # percentage
        percent_discarded = (discarded / aggregate) * 100
        percent_success = (success / aggregate) * 100

        # response
        return Response({"error": False, 'success': percent_success, 'discarded': percent_discarded}, status=status.HTTP_201_CREATED)


class SignalChartView(APIView):
    def get(self, request, format=None):
        channels = ['SMS', 'WHATSAPP', 'TELEGRAM', 'TWITTER', 'WEB', 'APP']

        arr_data = []
        for val in channels:
            #new
            new = Signal.objects.filter(channel=val, status='NEW').count()

            #success
            success = Signal.objects.filter(channel=val, status='ADDED').count()

            #discarded
            discarded = Signal.objects.filter(channel=val, status='DISCARDED').count()

            #create dict
            chart = {
                'name': val,
                'new': new,
                'success': success,
                'discarded': discarded
            }
            
            #append to arr_data
            arr_data.append(chart)

        #response
        return Response({"error": False, "chart" : arr_data}, status = status.HTTP_201_CREATED)


class EventPercentageChartView(APIView):
    def get(self, request, format=None):
        # events
        events = Event.objects

        # discarded events
        discarded = events.filter(status='DISCARED').count()

        #on progress
        on_progress = events.filter(status='PROGRESS').count()

        # closed events
        closed = events.filter(status='COMPLETE').count()

        # aggregate
        aggregate = discarded + closed + on_progress

        # percentage
        percent_discarded = 0
        percent_closed = 0
        percent_on_progress = 0

        if(aggregate != 0):
            percent_discarded = (discarded / aggregate) * 100
            percent_closed = (closed / aggregate) * 100
            percent_on_progress = (on_progress / aggregate) * 100

        # response
        return Response({"error": False, 'closed': percent_closed, 'discarded': percent_discarded, 'on_progress': percent_on_progress}, status=status.HTTP_201_CREATED)


class EventChartView(APIView):
    def get(self, request, format=None):
        sectors = Sector.objects.all()

        arr_data = []
        for val in sectors:
            #new
            new = Event.objects.filter(sector__id=val.id, status='NEW').count()

            #on progress
            progress = Event.objects.filter(sector__id=val.id, status='PROGRESS').count()

            #closed
            closed = Event.objects.filter(sector__id=val.id, status='COMPLETE').count()

            #discarded
            discarded = Event.objects.filter(sector__id=val.id, status='DISCARED').count()

            #create dict
            chart = {
                'name': val.title,
                'new': new,
                'progress': progress,
                'discarded': discarded,
                'closes': closed
            }
            
            #append to arr_data
            arr_data.append(chart)

        #response
        return Response({"error": False, "chart" : arr_data}, status = status.HTTP_201_CREATED)
      
