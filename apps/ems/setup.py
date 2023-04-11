from django.shortcuts import redirect, render
from .models import *

def get_districts(request, *args, **kwargs):
    if request.method == 'GET':
        region_id = kwargs['region_id']

        """Region"""
        region = Location.objects.get(pk=region_id)

        """districts"""
        districts = Location.objects.filter(path__istartswith=region.path, depth=3)

        """render view"""
        return render(None, 'setup/districts.html', {'districts': districts})
    

def get_wards(request, *args, **kwargs):
    if request.method == 'GET':
        district_id = kwargs['district_id']

        """district"""
        district = Location.objects.get(pk=district_id)

        """wards"""
        wards = Location.objects.filter(path__istartswith=district.path, depth=4)

        """render view"""
        return render(None, 'setup/wards.html', {'wards': wards})
    

def get_villages(request, *args, **kwargs):
    if request.method == 'GET':
        ward_id = kwargs['ward_id']

        """ward"""
        ward = Location.objects.get(pk=ward_id)

        """villages"""
        villages = Location.objects.filter(path__istartswith=ward.path, depth=5)

        """render view"""
        return render(None, 'setup/villages.html', {'villages': villages})