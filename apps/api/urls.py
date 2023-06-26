from django.urls import path
from . import views, users

urlpatterns = [
       
    path('reports/', views.ReportsList.as_view()),

    path('rumors/', views.RumorList.as_view()),
    path('rumors/validate', views.validateRumor.as_view(), name='validate-rumor'),
    path('rumors/confirm', views.confirmRumor.as_view(), name='confirm-rumor'),
    path('rumors/validity-notes/', views.RumorValidityNotes.as_view(), name='rumor-validity-notes'),
    path('rumors/attach2alert', views.attach_rumor2alert, name='attach2alert'),
    

    path('location', views.LocationList.as_view()),
    path('regions', views.RegionsList.as_view()),
    path('districts/<str:region_id>', views.DistrictsList.as_view()),
    path('wards/<str:district_id>', views.WardsList.as_view()),
    path('villages/<str:ward_id>', views.VillagesList.as_view()),
    path('validate-village', views.ValidateVillage.as_view(), name='validate-village'),

    path('sectors', views.SectorsList.as_view()),
    path('alert_types', views.AlertTypesList.as_view()),
    path('alerts', views.AlertList.as_view()),

    path('login/', users.LoginView.as_view()),
]