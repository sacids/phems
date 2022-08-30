from django.urls import path, include
from .views import *
from .charts import *

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('dashboard', DashboardView.as_view(), name='dashboard'),

    # chart
    path('percent-rate-chart', SignalPercentageChartView.as_view()),
    path('channel-rate-chart', SignalChartView.as_view()),

    #events
    path('event-percent-chart', EventPercentageChartView.as_view()),
    path('event-sectors-chart', EventChartView.as_view()),
]
