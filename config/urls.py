"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views
from apps.account import views as account_views
from apps.account import utils as api

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('apps.account.urls')),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/', api.registerUser, name='register'),
    path('api/activateOtp/', api.activateUser, name='activate'),
    path('api/me/', api.getMeView.as_view(), name='getMe'),
    path('webpush/', include('apps.webpush.urls')),
    path('chatbot/', include('apps.chatbot.urls')),
    path('ems/', include('apps.ems.urls')),

]
