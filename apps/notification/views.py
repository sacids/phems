from django.shortcuts import render
from django.core.mail import EmailMessage
from django.core.mail import BadHeaderError
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from .models import *


class MessageListView(generic.TemplateView):
    """ Messages Lists """
    template_name = "messages/lists.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(MessageListView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(MessageListView, self).get_context_data(**kwargs)
        return context
    

def mark_as_read(request, **kwargs):
    """mark notification as read"""
    message = Notification.objects.get(pk=kwargs['pk'])

    """change status"""
    message.app_status = "DELIVERED"
    message.save()

    """redirect with message"""
    messages.success(request, 'Notification marked as read')
    return HttpResponseRedirect(reverse_lazy('messages')) 