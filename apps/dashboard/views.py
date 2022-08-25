from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from apps.ems.models import Signal

# Create your views here.
@method_decorator(login_required, name='dispatch')
class DashboardView(View):
    template_name = 'dashboard.html'

    def get(self, request):
        no_of_signals = Signal.objects.count()
        no_of_new_signals = Signal.objects.filter(status='NEW').count()
        no_of_discarded_signals = Signal.objects.filter(status='DISCARDED').count()
        no_of_success_signals = Signal.objects.filter(status='ADDED').count()

         #context
        context = {
            'no_of_signals': no_of_signals,
            'no_of_new_signals': no_of_new_signals,
            'no_of_discarded_signals': no_of_discarded_signals,
            'no_of_success_signals': no_of_success_signals
            
        }

        return render(request, self.template_name, context)
