import json
from operator import ne
from unicodedata import name
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.db.models import Sum, Count
from apps.ems.models import Signal, Event, Sector, Location


class UpdateEventMapView(APIView):
    def get(self, request, format=None):
        with open('assets/json/map_regions.json', 'r') as f:
            data = json.load(f)

            arr_data = []
            for value in data['features']:
                regionName = value['properties']['name']

                region = Location.objects.filter(title=regionName)

                #print(region)

                if region:
                    #create array
                    arr = {
                        "type": "Feature", 
                        "geometry": value["geometry"],
                        "properties": {"name": regionName, "total_event": 0}
                    } 
                    arr_data.append(arr)  

                #update json
                data["type"] =  "FeatureCollection"
                data['features'] = arr_data;     

                #write to json file   
                with open('assets/json/map_regions.json', 'w') as json_file:
                    json.dump(data, json_file)          

        # response
        return Response({"error": False}, status=status.HTTP_201_CREATED)
