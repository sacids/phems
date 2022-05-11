from django.urls import path, include
from rest_framework import routers
from django.urls.resolvers import URLPattern
from .views import *
from . import api


router = routers.DefaultRouter()
router.register(r'signal', api.SignalViewSet)
router.register(r'keyword', api.KeywordViewSet)


urlpatterns = [
    path('api/', include(router.urls)),

    path('', EventListView.as_view(), name='events'),
    path('events', EventListView.as_view(), name='events'),
    path('signals', SignalListView.as_view(), name='signals'),
    path('overview', SignalListView.as_view(), name='overview'),
    path('dashboard', SignalListView.as_view(), name='dashboard'),
    path('files', SignalListView.as_view(), name='files'),
    path('messages', SignalListView.as_view(), name='messages'),
    path('timeline', SignalListView.as_view(), name='timeline'),
    path('calendar', SignalListView.as_view(), name='calendar'),
    
    
    
    path('utils/ps', promote_signal, name='promote_signal'),
    path('utils/ds', delete_signal, name='delete_signal'),
    path('utils/as', attach_sig2event, name='attach_sig2event'),
    path('utils/me', manage_event, name='manage_event'),
    path('utils/sl', search_location, name='search_location'),
    path('utils/ea', add_event, name='add_event'),

    #path('build', build_location_db)
    
]