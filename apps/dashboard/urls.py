from django.urls import path, include
from .views import *
from .charts import *
from .map import *

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('dashboard', DashboardView.as_view(), name='dashboard'),
    path('percent-rate-chart', SignalPercentageChartView.as_view()),
    path('channel-rate-chart', SignalChartView.as_view()),
    path('event-percent-chart', EventPercentageChartView.as_view()),
    path('event-sectors-chart', EventChartView.as_view()),
    path('alert-event-chart', AlertChartView.as_view()),
    path('update-event-map', UpdateEventMapView.as_view()),
]
