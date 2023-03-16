from django.urls import path, include
from rest_framework import routers
from django.urls.resolvers import URLPattern
from .views import *
from . import api

from . import ajax_datatable_views

router = routers.DefaultRouter()
router.register(r'signal', api.SignalViewSet)
router.register(r'keyword', api.KeywordViewSet)


urlpatterns = [
    path('api/', include(router.urls)),

    path('', SignalListView.as_view(), name='signals'),
    path('signals', SignalListView.as_view(), name='signals'),
    path('event_list', EventList2View.as_view(), name='event_list'),

    #events
    path('events', EventListView.as_view(), name='events'),
    path('event/<int:eid>', EventView.as_view(), name='event'),
    path('events/create', EventCreateView.as_view(), name='create-event'),
    path('events/<int:pk>/edit', EventUpdateView.as_view(), name='edit-event'),

    #rumors
    path('rumors', RumorListView.as_view(), name='rumors'),

    path('overview', SignalListView.as_view(), name='overview'),
    # path('dashboard', SignalListView.as_view(), name='dashboard'),
    path('files', SignalListView.as_view(), name='files'),
    path('messages', SignalListView.as_view(), name='messages'),
    path('reports', SignalListView.as_view(), name='reports'),
    path('calendar', SignalListView.as_view(), name='calendar'),
    
    path('utils/sitrep_form/<int:alert_id>/<int:form_id>', SitrepForm, name='sitrep_form'),
    
    
    
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
    path('utils/gec', get_colabs, name='get_colabs'),
    path('utils/aec', add_colabs, name='add_colabs'),
    path('utils/dec', del_colabs, name='del_colabs'),
    path('utils/ged', get_event_data, name='get_event_data'),
    path('utils/gad', get_alert_data, name='gad'),
    path('utils/cwf', change_wf, name='change_wf'),
    path('utils/uwf', update_wf, name='update_wf'),
    path('utils/su', search_users, name='search_users'),
    path('utils/mr', manage_rumor, name='manage_rumor'),
    
    path('utils/mea', manage_event_act, name='manage_event_act'),
    #path('utils/ssr', submit_sitreps, name='submit_sitreps'),

    #path('build', build_location_db)
    
    
    path('ajax_datatable/permissions/', ajax_datatable_views.PermissionAjaxDatatableView.as_view(), name="ajax_datatable_permissions"),
    path('ajax_datatable/event_list/', ajax_datatable_views.EventList.as_view(), name="e_list"),
    path('ajax_datatable/rumor_list/', ajax_datatable_views.RumorList.as_view(), name="r_list"),
    
]