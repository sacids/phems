from django.urls import path, include
from .views import *
from .charts import *

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),

    # chart
    path('percent-rate-chart', SignalPercentageChartView.as_view()),
    path('channel-rate-chart', SignalChartView.as_view()),
]
