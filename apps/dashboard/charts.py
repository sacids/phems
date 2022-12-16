import json
from operator import ne
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.db.models import Sum, Count
from apps.ems.models import Signal, Event, Sector, Alert

class SignalPercentageChartView(APIView):
    def get(self, request, format=None):
        """ Signals """
        signals = Signal.objects

        """Number of signals"""
        pending = signals.filter(status='NEW').count()
        discarded = signals.filter(status='DISCARDED').count()
        success = signals.filter(status='ADDED').count()
        aggregate = pending + discarded + success

        """Percentage"""
        percent_pending = (pending / aggregate) * 100
        percent_discarded = (discarded / aggregate) * 100
        percent_success = (success / aggregate) * 100

        """response"""
        return Response({"error": False, 'pending': percent_pending ,'success': percent_success, 'discarded': percent_discarded}, status=status.HTTP_201_CREATED)


class SignalChartView(APIView):
    def get(self, request, format=None):
        """channels"""
        channels = ['SMS', 'WHATSAPP', 'TELEGRAM', 'TWITTER', 'WEB', 'APP']

        arr_data = []
        for val in channels:
            """Number of signals"""
            new = Signal.objects.filter(channel=val, status='NEW').count()
            success = Signal.objects.filter(channel=val, status='ADDED').count()
            discarded = Signal.objects.filter(channel=val, status='DISCARDED').count()

            """dictionary"""
            chart = {
                'name': val,
                'new': new,
                'success': success,
                'discarded': discarded
            }
            
            """append dictionary"""
            arr_data.append(chart)

        """response"""
        return Response({"error": False, "chart" : arr_data}, status = status.HTTP_201_CREATED)


class EventPercentageChartView(APIView):
    def get(self, request, format=None):
        """Events"""
        events = Event.objects

        """Number of events"""
        discarded = events.filter(status='DISCARED').count()
        on_progress = events.filter(status='PROGRESS').count()
        closed = events.filter(status='COMPLETE').count()

        """aggregate data"""
        aggregate = discarded + closed + on_progress

        """Percentage"""
        percent_discarded = 0
        percent_closed = 0
        percent_on_progress = 0

        if(aggregate != 0):
            percent_discarded = (discarded / aggregate) * 100
            percent_closed = (closed / aggregate) * 100
            percent_on_progress = (on_progress / aggregate) * 100

        """response"""
        return Response({"error": False, 'closed': percent_closed, 'discarded': percent_discarded, 'on_progress': percent_on_progress}, status=status.HTTP_201_CREATED)


class EventChartView(APIView):
    def get(self, request, format=None):
        """sectors"""
        sectors = Sector.objects.all()

        arr_data = []
        for val in sectors:
            """Number of events"""
            new = Event.objects.filter(sector__id=val.id, status='NEW').count()
            progress = Event.objects.filter(sector__id=val.id, status='PROGRESS').count()
            closed = Event.objects.filter(sector__id=val.id, status='COMPLETE').count()
            discarded = Event.objects.filter(sector__id=val.id, status='DISCARED').count()

            """dictionary"""
            chart = {
                'name': val.title,
                'new': new,
                'progress': progress,
                'discarded': discarded,
                'closes': closed
            }
            
            """append dictionary"""
            arr_data.append(chart)

        """response"""
        return Response({"error": False, "chart" : arr_data}, status = status.HTTP_201_CREATED)


class AlertChartView(APIView):
    def get(self, request, format=None):
        """alerts"""
        alerts = Alert.objects.all()

        arr_data = []
        for val in alerts:
            """Number of events"""
            number_of_events = Event.objects.filter(alert__id=val.id).count()
            confirmed_number_of_events = Event.objects.filter(alert__id=val.id, stage__id=2).count()

            """dictionary"""
            chart = {
                'name': val.label,
                'number_of_events':  number_of_events,
                'confirmed_events': confirmed_number_of_events
            }
            
            """append dictionary"""
            arr_data.append(chart)

        """response"""
        return Response({"error": False, "chart" : arr_data}, status = status.HTTP_201_CREATED)
      
