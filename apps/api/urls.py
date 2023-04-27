from django.urls import path
from . import views, users

urlpatterns = [
       
    path('reports/', views.ReportsList.as_view()),

    path('rumors/', views.RumorList.as_view()),
    path('rumors/attach2alert', views.attach_rumor2alert, name='attach2alert'),
    path('rumors/discard', views.discard_rumor, name='discard-rumor'),
    path('rumors/confirm', views.confirm_rumor, name='confirm-rumor'),

    path('location', views.LocationList.as_view()),
    path('regions', views.RegionsList.as_view()),
    path('districts/<str:region_id>', views.DistrictsList.as_view()),
    path('wards/<str:district_id>', views.WardsList.as_view()),
    path('villages/<str:ward_id>', views.VillagesList.as_view()),

    path('sectors', views.SectorsList.as_view()),
    path('alert_types', views.AlertTypesList.as_view()),
    path('alerts', views.AlertList.as_view()),

    path('login/', users.LoginView.as_view()),
]