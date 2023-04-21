import json
from operator import ne
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.db.models import Sum, Count
from apps.ems.models import Signal, Event, Sector, Alert
from django.db.models import Q

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
        channels = ['SMS', 'USSD' , 'WHATSAPP', 'TELEGRAM', 'TWITTER', 'WEB', 'APP']

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
        if self.request.user.profile.level == "NATIONAL":
            new = events.filter(stage_id=1).count()
            confirmed = events.filter(stage_id=5).count()
            discarded = events.filter(stage_id=7).count()
            on_progress = events.filter(Q(stage_id=3) | Q(stage_id=4)).count()
        elif self.request.user.profile.level == "REGION": 
            new = events.filter(region_id=self.request.user.profile.region_id, stage_id=1).count()
            confirmed = events.filter(region_id=self.request.user.profile.region_id, stage_id=5).count()
            discarded = events.filter(region_id=self.request.user.profile.region_id,stage_id=7).count()
            on_progress = events.filter(Q(region_id=self.request.user.profile.region_id) & (Q(stage_id=3) | Q(stage_id=4))).count()
        elif self.request.user.profile.level == "DISTRICT": 
            new = events.filter(district_id=self.request.user.profile.district_id, stage_id=1).count()
            confirmed = events.filter(district_id=self.request.user.profile.district_id, stage_id=5).count()
            discarded = events.filter(district_id=self.request.user.profile.district_id, stage_id=7).count()
            on_progress = events.filter(Q(district_id=self.request.user.profile.district_id) & (Q(stage_id=3) | Q(stage_id=4))).count()  
       
        """aggregate data"""
        aggregate = new + discarded + confirmed + on_progress

        """Percentage"""
        percent_new = 0
        percent_discarded = 0
        percent_confirmed = 0
        percent_on_progress = 0

        if(aggregate != 0):
            percent_new = (new / aggregate) * 100
            percent_discarded = (discarded / aggregate) * 100
            percent_confirmed = (confirmed / aggregate) * 100
            percent_on_progress = (on_progress / aggregate) * 100

        """response"""
        return Response({"error": False, 'new': percent_new, 'confirmed': percent_confirmed, 'discarded': percent_discarded, 'on_progress': percent_on_progress}, status=status.HTTP_201_CREATED)


class EventChartView(APIView):
    def get(self, request, format=None):
        """sectors"""
        sectors = Sector.objects.all()

        arr_data = []
        for val in sectors:
            """Number of events"""
            events  = Event.objects

            if self.request.user.profile.level == "NATIONAL":
                new = events.filter(sector__id=val.id, stage_id=1).count()
                progress = events.filter(Q(stage_id=3) | Q(stage_id=4)).filter(sector__id=val.id).count()
                confirmed = events.filter(sector__id=val.id, stage_id=5).count()
                discarded = events.filter(sector__id=val.id, stage_id=7).count()

            elif self.request.user.profile.level == "REGION": 
                new = events.filter(sector__id=val.id, region_id=self.request.user.profile.region_id, stage_id=1).count()
                progress = events.filter(Q(stage_id=3) | Q(stage_id=4)).filter(sector__id=val.id, region_id=self.request.user.profile.region_id).count()
                confirmed = events.filter(sector__id=val.id, stage_id=5, region_id=self.request.user.profile.region_id).count()
                discarded = events.filter(sector__id=val.id, stage_id=7, region_id=self.request.user.profile.region_id).count()

            elif self.request.user.profile.level == "DISTRICT": 
                new = events.filter(sector__id=val.id, district_id=self.request.user.profile.district_id, stage_id=1).count()
                progress = events.filter(Q(stage_id=3) | Q(stage_id=4)).filter(sector__id=val.id, district_id=self.request.user.profile.district_id).count()
                confirmed = events.filter(sector__id=val.id, district_id=self.request.user.profile.district_id, stage_id=5).count()
                discarded = events.filter(sector__id=val.id, district_id=self.request.user.profile.district_id, stage_id=7).count()


            """dictionary"""
            chart = {
                'name': val.title,
                'new': new,
                'progress': progress,
                'discarded': discarded,
                'confirmed': confirmed
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
            events  = Event.objects

            if self.request.user.profile.level == "NATIONAL":
                number_of_events = events.filter(alert__id=val.id).count()
                confirmed_number_of_events = events.filter(alert__id=val.id, stage_id=5).count()
            elif self.request.user.profile.level == "REGION":
                number_of_events = events.filter(alert__id=val.id, region_id=self.request.user.profile.region_id).count()
                confirmed_number_of_events = events.filter(alert__id=val.id, stage_id=5, region_id=self.request.user.profile.region_id).count() 
            elif self.request.user.profile.level == "DISTRICT":
                number_of_events = events.filter(alert__id=val.id, district_id=self.request.user.profile.district_id).count()
                confirmed_number_of_events = events.filter(alert__id=val.id, stage_id=5, district_id=self.request.user.profile.district_id).count()

            """dictionary"""
            chart = {
                'name': val.label,
                'number_of_events':  number_of_events,
                'confirmed_events': confirmed_number_of_events
            }
            
            """append dictionary"""
            arr_data.append(chart)

        """response"""
        return Response({"error": False, "chart" : arr_data}, status = status.HTTP_200_OK)
      
