import json
from operator import ne
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.db.models import Sum, Count
from apps.ems.models import Signal, Event, Sector


class UpdateEventMapView(APIView):
    def get(self, request, format=None):
        with open('assets/json/map_regions.json', 'r') as f:
            data = json.load(f)

            for value in data['features']:
                regionName = value['properties']['name']

                

                print(regionName)


        # response
        return Response({"error": False}, status=status.HTTP_201_CREATED)
