from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from apps.ems.models import Signal, Event
from django.db.models import Q

# Create your views here.
@method_decorator(login_required, name='dispatch')
class DashboardView(View):
    template_name = 'dashboard.html'

    def get(self, request):
        """Number of signals"""
        signals = Signal.objects
        no_of_signals = signals.count()
        no_of_new_signals = signals.filter(status='NEW').count()
        no_of_discarded_signals = signals.filter(status='DISCARDED').count()
        no_of_success_signals = signals.filter(status='ADDED').count()

        """Number of events"""
        events = Event.objects

        if self.request.user.profile.level == "NATIONAL":
            no_of_new_events = events.filter(stage_id=1).count()
            no_of_discarded_events = events.filter(stage_id=7).count()
            no_of_comfirmed_events = events.filter(stage_id=5).count()
            no_of_progress_events = events.filter(Q(stage_id=3) | Q(stage_id=4)).count()

        elif self.request.user.profile.level == "REGION":
            no_of_new_events = events.filter(region_id=self.request.user.profile.region_id, stage_id=1).count()
            no_of_discarded_events = events.filter(region_id=self.request.user.profile.region_id, stage_id=7).count()
            no_of_comfirmed_events = events.filter(region_id=self.request.user.profile.region_id, stage_id=5).count()
            no_of_progress_events = events.filter(Q(region_id=self.request.user.profile.region_id) & (Q(stage_id=3) | Q(stage_id=4))).count()

        elif self.request.user.profile.level == "DISTRICT":
            no_of_new_events = events.filter(district_id=self.request.user.profile.district_id, stage_id=1).count()
            no_of_discarded_events = events.filter(district_id=self.request.user.profile.district_id, stage_id=7).count()
            no_of_comfirmed_events = events.filter(district_id=self.request.user.profile.district_id, stage_id=5).count()
            no_of_progress_events = events.filter(Q(district_id=self.request.user.profile.district_id) & (Q(stage_id=3) | Q(stage_id=4))).count()


        """Passing data to views"""
        context = {
            'no_of_signals': no_of_signals,
            'no_of_new_signals': no_of_new_signals,
            'no_of_discarded_signals': no_of_discarded_signals,
            'no_of_success_signals': no_of_success_signals,
            'no_of_new_events' : no_of_new_events,
            'no_of_progress_events' : no_of_progress_events,
            'no_of_comfirmed_events' : no_of_comfirmed_events, 
            'no_of_discarded_events' : no_of_discarded_events, 
        }

        return render(request, self.template_name, context)
