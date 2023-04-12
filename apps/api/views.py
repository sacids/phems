from apps.ems.models import *
from .serializers import AlertSerializer
from django.http import Http404, JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime


# Create your views here.
class AlertTypesList(APIView):
    """API to fetch alert types"""
    def get(self, request, format=None):
        alert_types = Alert.objects.all()

        arr_data = []
        for val in alert_types:
            """create dict"""
            chart = {
                'id': val.id,
                'reference': val.reference,
                'label': val.label,
                'title': val.title,
                'primary_sector': val.pri_sector.title
            } 
            """append to arr_data"""
            arr_data.append(chart)

        return Response(arr_data, status = status.HTTP_200_OK)

class LocationList(APIView):
    """API to fetch location"""
    def get(self, request, format=None):
        location = Location.objects.filter(depth=2).order_by('title')

        arr_data = []
        for val in location:
            """create dict"""
            chart = {
                'id': val.id,
                'code': val.code,
                'title': val.title,
            } 
            """append to arr_data"""
            arr_data.append(chart)

        return Response(arr_data, status = status.HTTP_200_OK)
    
class RegionsList(APIView):
    """API to fetch regions"""
    def get(self, request, format=None):
        location = Location.objects.filter(depth=2).order_by('title')

        arr_data = []
        for val in location:
            """create dict"""
            chart = {
                'id': val.id,
                'code': val.code,
                'title': val.title,
            } 
            """append to arr_data"""
            arr_data.append(chart)

        return Response(arr_data, status = status.HTTP_200_OK)
    

class DistrictsList(APIView):
    """API to fetch districts"""
    def get(self, request, *args, **kwargs):
        region_id = kwargs.get("region_id")

        """Region"""
        region = Location.objects.get(pk=region_id)

        """districts"""
        districts = Location.objects.filter(path__istartswith=region.path, depth=3).order_by('title')

        arr_data = []
        for val in districts:
            """create dict"""
            chart = {
                'id': val.id,
                'code': val.code,
                'title': val.title,
            } 
            """append to arr_data"""
            arr_data.append(chart)

        return Response(arr_data, status = status.HTTP_200_OK)
    
class WardsList(APIView):
    """API to fetch wards"""
    def get(self, request, *args, **kwargs):
        district_id = kwargs.get("district_id")

        """District"""
        district = Location.objects.get(pk=district_id)

        """wards"""
        wards = Location.objects.filter(path__istartswith=district.path, depth=4)

        arr_data = []
        for val in wards:
            """create dict"""
            chart = {
                'id': val.id,
                'code': val.code,
                'title': val.title,
            } 
            """append to arr_data"""
            arr_data.append(chart)

        return Response(arr_data, status = status.HTTP_200_OK)
    

class VillagesList(APIView):
    """API to fetch wards"""
    def get(self, request, *args, **kwargs):
        ward_id = kwargs.get("ward_id")

        """District"""
        ward = Location.objects.get(pk=ward_id)

        """villages"""
        villages = Location.objects.filter(path__istartswith=ward.path, depth=5)

        arr_data = []
        for val in villages:
            """create dict"""
            chart = {
                'id': val.id,
                'code': val.code,
                'title': val.title,
            } 
            """append to arr_data"""
            arr_data.append(chart)

        return Response(arr_data, status = status.HTTP_200_OK)


class SectorsList(APIView):
    """API to fetch sectors"""
    def get(self, request, format=None):
        sectors = Sector.objects.all()

        arr_data = []
        for val in sectors:
            """create dict"""
            chart = {
                'id': val.id,
                'title': val.title,
            } 
            """append to arr_data"""
            arr_data.append(chart)

        return Response(arr_data, status = status.HTTP_200_OK)


class AlertList(APIView):
    """API to fetch alerts"""
    def get(self, request, format = None):
        """alerts"""
        alerts = Event.objects   

        if self.request.user.profile.level == 'NATIONAL':
            alerts = alerts.all().order_by('-pk')

        elif self.request.user.profile.level == 'REGION': 
            alerts = alerts.filter(region_id=self.request.user.profile.region_id).order_by('-pk')

        elif self.request.user.profile.level == 'DISTRICT': 
            alerts = alerts.filter(district_id=self.request.user.profile.district_id).order_by('-pk')
   
        arr_data = []
        for alert in alerts:
            """create dict"""
            chart = {
                'id': alert.id,
                'title': alert.title,
                'description': alert.description,
                'status': alert.status,
                'created_on': date.strftime(alert.created_on, '%d/%m/%Y %H:%M'),
                'stage': alert.stage.title,
                'alert_type_label': alert.alert.label,
                'alert_type_title': alert.alert.title,
                'primary_sector': alert.pri_sector.title
            } 

            if alert.region_id is not None:
                chart['region'] = alert.region.title

            if alert.district_id is not None:
                chart['district'] = alert.district.title

            if alert.ward_id is not None:
                chart['ward'] = alert.ward.title

            if alert.village_id is not None:
                chart['village'] = alert.village.title

            """append to arr_data"""
            arr_data.append(chart)

        return Response(arr_data, status = status.HTTP_200_OK)

    def post(self, request, format=None):
        """create new alert"""
        new_alert = Event()
        new_alert.title         = request.POST.get('title')
        new_alert.description   = request.POST.get('description')
        new_alert.alert_id      = request.POST.get('alert_type_id')
        # new_alert.location_id   = request.POST.get('location_id')
        new_alert.pri_sector_id = request.POST.get('primary_sector_id')
        new_alert.save()

        if new_alert:
            return Response({"error": False, "success_msg": "Alert created!"}, status = status.HTTP_201_CREATED)
        else:
            return Response({"error": True, "error_msg": "Failed to create alert!"}, status = status.HTTP_400_BAD_REQUEST) 


class RumorList(APIView):
    """API to fetch rumors""" 
    def get(self, request, format=None):
        rumors = Signal.objects.filter(status="NEW").order_by('-created_on','-relevance')

        arr_data = []
        for rumor in rumors:
            """create dictionary"""
            chart = {
                'id': rumor.id,
                'title': rumor.contents['text'],
                'channel': rumor.channel,
                'status': rumor.status,
                'created_on': date.strftime(rumor.created_on, '%d/%m/%Y %H:%M'),
                'relevance': rumor.relevance,
                'contact': rumor.contact,
            } 
            """append to arr_data"""
            arr_data.append(chart)

        return Response(arr_data, status = status.HTTP_200_OK)


    def post(self, request, format=None):
        serializer = AlertSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST) 


def discard_rumor(request):
    """discard rumors""" 
    rumor_id = request.GET.get('rid', 0)

    """rumor"""
    rumor = Signal.objects.get(pk=rumor_id)
    rumor = 'DISCARDED'
    rumor.save()

    """return response"""
    return JsonResponse({"error": False, "success_msg": "Rumor discarded"}, safe=False)  


def attach_rumor2alert(request):
    """attach rumor to alert"""
    rumor_id   = request.GET.get('rid',0) 
    alert_id   = request.GET.get('aid',0)
    
    signal   = Signal.objects.get(pk=rumor_id)
    alert   = Event.objects.get(pk=alert_id)
    
    """attach rumor 2 alert"""
    alert.signal.add(signal)
    
    """change rumor status"""
    signal.status = 'ADDED'
    signal.save()
    
    """return response"""
    return JsonResponse({"error": False, "success_msg": "Rumor added to alert"}, safe=False)         


class ReportsList(APIView):
    """API to fetch situation reports""" 
    def get(self, request, format=None):
        arr_data = []

        """create dictionary"""
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