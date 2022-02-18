from django.urls import path
from django.urls.resolvers import URLPattern
from .views import LogoutView, RegistrationView, LoginView ,ActivateAccount

urlpatterns = [
    path("register/", RegistrationView.as_view(), name="register"),
    path('activate/<uidb64>/<token>/', ActivateAccount.as_view(), name='activate'),
    path("login/", LoginView.as_view() , name="login"),  
    path("logout/", LogoutView.as_view(), name="logout"),
]