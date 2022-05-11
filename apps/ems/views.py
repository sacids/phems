from django.shortcuts import redirect, render
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import *
from .models import *
from django.views import generic
from django.http import HttpResponse, JsonResponse
from django.template.response import TemplateResponse
from .forms import *

# Create your views here.

class EventListView(generic.ListView):
    model               = Event
    context_object_name = 'events'
    template_name       = "events/list.html"


class SignalListView(generic.TemplateView):
    template_name       = "events/signals.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/auth/login/')
        return super(SignalListView, self).dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):

        context = super(SignalListView, self).get_context_data(**kwargs)
        context['signals']      = Signal.objects.filter(status='NEW')
        return context


















def delete_signal(request):
    sig_id              = request.GET.get('sid',0)
    sig_obj             = Signal.objects.get(pk=sig_id)
    sig_obj.status      = 'DISCARDED'
    sig_obj.save()
    return JsonResponse(1,safe=False)
    


def promote_signal(request):
    
    sig_id              = request.GET.get('sid',0) 
    
    context             = {}
    context['signal']   = Signal.objects.get(pk=sig_id)
    context['events']   = Event.objects.all()
    context['sectors']  = Sector.objects.all()
    context['profession']   = Event.PROFESSION
    

    template            = 'events/async/promote_signal.html'
    
    return TemplateResponse(request,template,context)

def add_event(request):
    
    form                = EventForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        # save the form data to model
        form.save()
    return JsonResponse("Event Add success",safe=False)

def manage_event(request):
    
    eid                 = request.GET.get('eid',0) 
    
    context             = {}
    context['event']   = Event.objects.get(pk=eid)

    template            = 'events/async/manage_event.html'
    
    return TemplateResponse(request,template,context)

def attach_sig2event(request):
    
    sig_id              = request.GET.get('sid',0) 
    evt_id              = request.GET.get('eid',0)
    
    event   = Event.objects.get(pk=evt_id)
    signal  = Signal.objects.get(pk=sig_id)
    event.signal.add(signal)
    
    # if attache success
    signal.status = 'ADDED'
    signal.save()
    
    return JsonResponse("Attach success",safe=False)



def search_location(request):
    
    term        = request.GET.get('term',0) 
    node        = Location.objects.filter(title__icontains=term)
    
    data        = []
    for item in node:
        par     = item.get_parent()
        
        tmp     = {}
        tmp['id']   = item.id
        text        = par.title+' - '+item.title
        tmp['text'] = (text.replace("'", "")).lower().title()
        data.append(tmp)
        
    results    = {}
    results['results']  = data
    
    return JsonResponse(results,safe=False)
    
    












def get_list(list_name):
    with open("assets/json/location/"+list_name+".json", 'r') as file:
        regions = json.loads(file.read().rstrip())

    return JsonResponse(1,safe=False)


















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