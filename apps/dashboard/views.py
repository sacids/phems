from multiprocessing import Event
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from apps.ems.models import Signal, Event

# Create your views here.
@method_decorator(login_required, name='dispatch')
class DashboardView(View):
    template_name = 'dashboard.html'

    def get(self, request):
        """Number of signals"""
        no_of_signals = Signal.objects.count()
        no_of_new_signals = Signal.objects.filter(status='NEW').count()
        no_of_discarded_signals = Signal.objects.filter(status='DISCARDED').count()
        no_of_success_signals = Signal.objects.filter(status='ADDED').count()

        """Number of events"""
        no_of_new_events = Event.objects.filter(status='NEW').count()
        no_of_discarded_events = Event.objects.filter(status='DISCARED').count()
        no_of_closed_events = Event.objects.filter(status='COMPLETE').count()
        no_of_progress_events = Event.objects.filter(status='PROGRESS').count()

        """Passing data to views"""
        context = {
            'no_of_signals': no_of_signals,
            'no_of_new_signals': no_of_new_signals,
            'no_of_discarded_signals': no_of_discarded_signals,
            'no_of_success_signals': no_of_success_signals,
            'no_of_new_events' : no_of_new_events,
            'no_of_progress_events' : no_of_progress_events,
            'no_of_discarded_events' : no_of_discarded_events,
            'no_of_closed_events' : no_of_closed_events   
        }

        return render(request, self.template_name, context)
