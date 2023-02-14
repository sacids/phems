from django.urls import path
from . import views, users

urlpatterns = [
    path('alerts/', views.AlertList.as_view()),   
    path('reports/', views.ReportsList.as_view()),
    path('rumors/', views.RumorList.as_view()),

    path('login/', users.LoginView.as_view()),
]