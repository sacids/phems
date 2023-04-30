import logging

from django.http import Http404, JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from django.db.models import Sum, F, Q
from apps.ems.models import *
from apps.account.models import Profile
from .serializers import AlertSerializer

from django.contrib.sites.shortcuts import get_current_site
from apps.notification.classes import NotificationWrapper
from apps.notification.tasks import send_email


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
        """get variables"""
        level = self.request.GET.get("level")
        region_id = self.request.GET.get("region_id")
        district_id = self.request.GET.get("district_id")
        ward_id = self.request.GET.get("ward_id")

        """alerts"""
        alerts = Event.objects

        """filtering per level"""
        if level == 'NATIONAL':
            alerts = alerts.all().order_by('-pk')

        elif level == 'REGION': 
            alerts = alerts.filter(region_id=region_id).order_by('-pk')

        elif level == 'DISTRICT': 
            alerts = alerts.filter(district_id=district_id).order_by('-pk')

        elif level == 'WARD': 
            alerts = alerts.filter(ward_id=ward_id).order_by('-pk')

        else:
            alerts = alerts.all().order_by('-pk')    
   
        arr_data = []
        for alert in alerts:
            """check region"""
            region_name = ""
            if alert.region is not None:
                region_name = alert.region.title

            """stage"""
            stage_name = ""
            if alert.stage is not None:
                stage_name = alert.stage.title

            """create dict"""
            chart = {
                'id': alert.id,
                'title': alert.title,
                'description': alert.description,
                'status': alert.status,
                'location': region_name,
                'created_on': date.strftime(alert.created_on, '%d/%m/%Y %H:%M'),
                'stage': stage_name,
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
        """get variables"""
        level = self.request.GET.get("level")
        region_id = self.request.GET.get("region_id")
        district_id = self.request.GET.get("district_id")
        ward_id = self.request.GET.get("ward_id")

        rumors = Signal.objects.exclude(relevance=0).filter(Q(status="NEW") | Q(status="CONFIRMED") | Q(status="DISCARDED")).order_by('-created_on','-relevance')

        """filtering per level"""
        if level == 'NATIONAL':
            rumors = rumors

        elif level == 'REGION': 
            rumors = rumors.filter(region_id=region_id)

        elif level == 'DISTRICT': 
            rumors = rumors.filter(district_id=district_id)

        elif level == 'WARD': 
            rumors = rumors.filter(ward_id=ward_id)

        arr_data = []
        for rumor in rumors:
            """rumor content"""
            title = ""
            if 'text' in rumor.contents:
                title = rumor.contents['text']  

            occurance_date = ""
            if 'date' in rumor.contents:
                occurance_date = rumor.contents['date']  

            region = ""
            if rumor.region is not None:
                region = rumor.region.title    

            district = ""
            if rumor.district is not None:
                district = rumor.district.title  

            ward = ""
            if rumor.ward is not None:
                ward = rumor.ward.title

            village = ""
            if rumor.village is not None:
                village = rumor.village.title 

            confirmed_by = ""
            if rumor.confirmed_by is not None:
                confirmed_by = rumor.confirmed_by.first_name + " " + rumor.confirmed_by.last_name  

            confirmed_on = ""
            if rumor.confirmed_on is not None:
                confirmed_on = date.strftime(rumor.confirmed_on, '%d/%m/%Y %H:%M') 

            """create dictionary"""
            chart = {
                'id': rumor.id,
                'relevance': rumor.relevance,
                'title': title,
                'channel': rumor.channel,
                'occurance_on': occurance_date,
                'created_on': date.strftime(rumor.created_on, '%d/%m/%Y %H:%M'),
                'contact': rumor.contact,
                'region': region,
                'district': district,
                'ward': ward,
                'village': village,
                'popular_area': village,
                'status': rumor.status,
                'confirmed_by': confirmed_by,
                'confirmed_on': confirmed_on   
            } 
            """append to arr_data"""
            arr_data.append(chart)

        return Response(arr_data, status = status.HTTP_200_OK)


    def post(self, request, format=None):
        """data contents"""
        contents = request.data['contents']
        contact  = request.data['contact']
        channel  = request.data['channel']

        """base url"""
        fullURL = ''.join(['http://', get_current_site(self.request).domain, reverse('rumors')])

        """notification wrapper"""
        notify = NotificationWrapper()

        """Find exact location of rumor"""
        if 'village' in contents:
            village_name = contents['village']

            """query for village"""
            village = Location.objects.filter(depth=5, title__icontains=village_name, path__startswith='0001000O')

            if village.count() > 0:
                """declare location data"""
                ward_id = None
                district_id = None
                region_id = None

                if village.count() == 1:
                    village  = village.first() #village
                    ward     = village.get_parent() #ward
                    district = ward.get_parent() #district
                    region   = district.get_parent() #region

                    """assign variable"""
                    ward_id     = ward.id
                    district_id = district.id
                    region_id   = region.id

                    """saving rumor data """
                    new_signal = Signal()
                    new_signal.channel     = channel
                    new_signal.contact     = contact
                    new_signal.contents    = contents
                    new_signal.region_id   = region.id
                    new_signal.district_id = district.id
                    new_signal.ward_id     = ward.id
                    new_signal.village_id  = village.id
                    new_signal.save()     
  
                elif village.count() > 1:
                    if 'ward' in contents:
                        ward_name = contents['ward']

                        """query for ward"""
                        ward = Location.objects.filter(depth=4, title__icontains=ward_name, path__startswith='0001000O')

                        if ward.count() > 0:
                            if ward.count() == 1:
                                ward = ward.first() #ward
                                district = ward.get_parent() #district
                                region = district.get_parent() #region

                                """assign variable"""
                                ward_id     = ward.id
                                district_id = district.id
                                region_id   = region.id

                                """saving rumor data """
                                new_signal = Signal()
                                new_signal.channel     = channel
                                new_signal.contact     = contact
                                new_signal.contents    = contents
                                new_signal.region_id   = region.id
                                new_signal.district_id = district.id
                                new_signal.ward_id     = ward.id
                                new_signal.save()
                
                """create message"""
                message_to_users = f"Taarifa Mpya. Tafadhali ingia kwenye mfumo kuifanyia kazi. Taarifa: {contents}"

                """send notification to ward supervisor"""
                profile = Profile.objects.filter(ward_id=ward_id, level='WARD')

                if profile.count() > 0:
                    arr_users = []
                    for val in profile:
                        """create notification"""
                        response = notify.create_notification(
                            user_id = val.user.id, 
                            created_by = 1,
                            message=message_to_users,
                            url = fullURL
                        )

                        """assign to array"""
                        arr_users.append(val.user.email)

                        """send sms"""
                        arr_phone = []
                        phone = notify.cast_phone_number(phone=val.phone)
                        recipient = {"recipient_id": 1, "dest_addr": phone}
                        arr_phone.append(recipient)

                        """array data"""
                        arr_data = {"source_addr": "TAARIFA", "schedule_time": "", "encoding": "0", "message": message_to_users, "recipients": arr_phone}

                        result = notify.send_sms(arr_data)
                        data = json.loads(result.content) 

                    """send email in background"""
                    # response = send_email("OHP: New Rumor" , message_to_users, arr_users)
                else:  
                    """send notification to district supervisors"""
                    profile = Profile.objects.filter(district_id=district_id, level='DISTRICT')

                    if profile.count() > 0:
                        arr_users = []
                        for val in profile:
                            """create notification"""
                            response = notify.create_notification(
                                user_id = val.user.id, 
                                created_by = 1,
                                message=message_to_users,
                                url = fullURL
                            )

                            """assign to array"""
                            arr_users.append(val.user.email)

                            """send sms"""
                            arr_phone = []
                            phone = notify.cast_phone_number(phone=val.phone)
                            recipient = {"recipient_id": 1, "dest_addr": phone}
                            arr_phone.append(recipient)

                            """array data"""
                            arr_data = {"source_addr": "TAARIFA", "schedule_time": "", "encoding": "0", "message": message_to_users, "recipients": arr_phone}

                            result = notify.send_sms(arr_data)
                            data = json.loads(result.content) 

                        """send email in background"""
                        # response = send_email("OHP: New Rumor" , message_to_users, arr_users)  
                    else:
                        """send notification to region supervisors"""
                        profile = Profile.objects.filter(region_id=region_id, level='REGION')

                        if profile.count() > 0:
                            arr_users = []
                            for val in profile:
                                """create notification"""
                                response = notify.create_notification(
                                    user_id = val.user.id, 
                                    created_by = 1,
                                    message=message_to_users,
                                    url = fullURL
                                )

                                """assign to array"""
                                arr_users.append(val.user.email)

                                """send sms"""
                                arr_phone = []
                                phone = notify.cast_phone_number(phone=val.phone)
                                recipient = {"recipient_id": 1, "dest_addr": phone}
                                arr_phone.append(recipient)

                                """array data"""
                                arr_data = {"source_addr": "TAARIFA", "schedule_time": "", "encoding": "0", "message": message_to_users, "recipients": arr_phone}

                                result = notify.send_sms(arr_data)
                                data = json.loads(result.content) 

                            """send email in background"""
                            # response = send_email("OHP: New Rumor" , message_to_users, arr_users)            
            else:
                """saving rumor data """
                new_signal = Signal()
                new_signal.channel     = channel
                new_signal.contact     = contact
                new_signal.contents    = contents
                new_signal.save()
        else:
            """saving rumor data """
            new_signal = Signal()
            new_signal.channel     = channel
            new_signal.contact     = contact
            new_signal.contents    = contents
            new_signal.save()

        """response"""
        return Response({'error': False, 'success_msg': 'Rumor created'}, status = status.HTTP_200_OK) 


def confirm_rumor(request):
    """confirm rumors""" 
    rumor_id = request.GET.get('sid', 0)
    confirmed_by  = request.GET.get('uid', 0)

    """rumor"""
    rumor = Signal.objects.get(pk=rumor_id)
    rumor.status = 'CONFIRMED'
    rumor.confirmed_by_id = confirmed_by
    rumor.relevance = 100
    rumor.save()

    logging.info(rumor)

    """return response"""
    return JsonResponse({"error": False, "success_msg": "Rumor confirmed"}, safe=False)  


def discard_rumor(request):
    """discard rumors""" 
    rumor_id = request.GET.get('sid', 0)

    """rumor"""
    rumor = Signal.objects.get(pk=rumor_id)
    rumor.status = 'DISCARDED'
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
    signal.status = "ADDED"
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