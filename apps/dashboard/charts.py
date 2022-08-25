import json
from operator import ne
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.db.models import Sum, Count
from apps.ems.models import Signal

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
