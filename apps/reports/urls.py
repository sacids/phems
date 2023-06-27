from django.urls import path
from .views import *



urlpatterns = [
    path('reports/events', EventReportView.as_view(), name='event-report'),

]