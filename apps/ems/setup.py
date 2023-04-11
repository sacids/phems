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