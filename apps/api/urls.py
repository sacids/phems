from django.urls import path
from . import views

urlpatterns = [
    path('alerts/', views.AlertList.as_view()),   
    path('rumors/', views.RumorList.as_view()),
]