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

    path('', SignalListView.as_view(), name='signals'),
    path('events', EventListView.as_view(), name='events'),
    #path('oevents', EventListView2.as_view(), name='oevents'),
    path('signals', SignalListView.as_view(), name='signals'),
    path('overview', SignalListView.as_view(), name='overview'),
    # path('dashboard', SignalListView.as_view(), name='dashboard'),
    path('files', SignalListView.as_view(), name='files'),
    path('messages', SignalListView.as_view(), name='messages'),
    path('reports', SignalListView.as_view(), name='reports'),
    path('calendar', SignalListView.as_view(), name='calendar'),
    
    
    
    path('utils/ps', promote_signal, name='promote_signal'),
    path('utils/ds', delete_signal, name='delete_signal'),
    path('utils/di', delete_item, name='delete_item'),
    path('utils/as', attach_sig2event, name='attach_sig2event'),
    path('utils/me', manage_event, name='manage_event'),
    path('utils/sl', search_location, name='search_location'),
    path('utils/ae', add_event, name='add_event'),
    path('utils/uf', upload_file, name='upload_file'),
    path('utils/gf', get_files, name='get_files'),
    path('utils/an', add_note, name='add_note'),
    path('utils/gn', get_notes, name='get_notes'),
    path('utils/ged', get_event_data, name='get_event_data'),
    path('utils/cwf', change_wf, name='change_wf'),
    path('utils/uwf', update_wf, name='update_wf'),
    
    path('utils/mea', manage_event_act, name='manage_event_act'),

    #path('build', build_location_db)
    
]