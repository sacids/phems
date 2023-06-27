from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import View, ListView
from apps.ems.models import *
from django.db.models import Q
from django.contrib.sites.shortcuts import get_current_site

# Create your views here.
# Create your views here.
@method_decorator(login_required, name='dispatch')
class EventReportView(ListView):
    context_object_name = "alerts"
    template_name = 'events.html'

    def get_context_data(self, **kwargs):
        context = super(EventReportView, self).get_context_data(**kwargs)

        context['sectors'] = Sector.objects.all()
        context['alert_types'] = Alert.objects.all()
        context['signal_keys'] = SignalKeys.objects.all()
        context['regions'] = Location.objects.filter(depth=2).order_by("title")

        return context
    
    def get_queryset(self):
        start_at = self.request.GET.get("start_at")
        end_at = self.request.GET.get("end_at")
        signal_key_id = self.request.GET.get("signal_key_id")
        alert_type_id = self.request.GET.get("alert_type_id")
        pri_sector_id = self.request.GET.get("pri_sector_id")
        region_id = self.request.GET.get("region_id")
        district_id = self.request.GET.get("district_id")
        ward_id = self.request.GET.get("ward_id")
        village_id = self.request.GET.get("village_id")

        #alerts
        alerts = Event.objects.order_by('-created_on')

        if  start_at and end_at:
            alerts = alerts.filter(
                created_on__range=[start_at, end_at])
            
        if alert_type_id:
            alerts = alerts.filter(alert_id=alert_type_id)

        if pri_sector_id:
            alerts = alerts.filter(pri_sector_id=pri_sector_id)    
            
        if region_id:
            alerts = alerts.filter(region_id=region_id)

        if district_id:
            alerts = alerts.filter(district_id=district_id)

        if ward_id:
            alerts = alerts.filter(ward_id=ward_id)

        if village_id:
            alerts = alerts.filter(village_id=village_id) 

        return alerts         

    

