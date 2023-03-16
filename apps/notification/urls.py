from django.urls import path
from .views import *

urlpatterns = [
    path('messages', MessageListView.as_view(), name='messages'),
    path('<int:pk>/mark-as-done', mark_as_read, name='mark-as-done'),
]