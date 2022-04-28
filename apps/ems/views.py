from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import *
from .models import *
from django.views import generic
from django.http import HttpResponse, JsonResponse

# Create your views here.


class EventListView(generic.ListView):
    model = Event
    template_name = "events/list.html"


class SignalListView(generic.ListView):
    model = Signal
    template_name = "events/signals.html"

    def get_context_data(self, **kwargs):

        context = super(SignalListView, self).get_context_data(**kwargs)
        context['keywords']     = SignalKeys.objects.all()
        return context

















def get_list(list_name):
    with open("assets/json/location/"+list_name+".json", 'r') as file:
        regions = json.loads(file.read().rstrip())

    return regions


















"""
def build_location_db(request):

    root        = Location.objects.get(pk=1)
    regions     = get_list('regions')
    districts   = get_list('districts')
    wards       = get_list('wards')
    villages    = get_list('villages')

    for region in regions:
        r_node    = root.add_child(title=region['name'],code=region['code'],p_id='r_'+(str(region['id'])).strip())
    
    for district in districts:
        r_id      = 'r_'+str(district['region_id'])
        try:
            r_node    = Location.objects.get(p_id=r_id.strip())
            r_node.add_child(title=district['name'],code=soundex(district['name']),p_id='d_'+str(district['id']).strip())
        except Location.DoesNotExist:
            print('District '+r_id)

    for ward in wards:
        d_id      = 'd_'+str(ward['district_id'])
        try:
            d_node    = Location.objects.get(p_id=d_id.strip())
            w_node    = d_node.add_child(title=ward['name'],code=soundex(ward['name']),p_id='w_'+(str(ward['id'])).strip())
        except Location.DoesNotExist:
            print('Ward '+d_id)

    for village in villages:
        w_id      = 'w_'+str(village['ward_id'])
        try:
            w_node    = Location.objects.get(p_id=w_id.strip())
            v_node    = w_node.add_child(title=village['name'],code=soundex(village['name']),p_id='v_'+(str(village['id'])).strip())
        except Location.DoesNotExist:
            print('Village '+w_id)


    return HttpResponse('moja')
"""