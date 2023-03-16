from django.urls import path
from django.urls.resolvers import URLPattern
from .views import LogoutView, RegistrationView, LoginView ,ActivateAccount, ProfileView, ChangePasswordView
from django.contrib.auth import views as auth_views
from . import users as views

urlpatterns = [
    path("register/", RegistrationView.as_view(), name="register"),
    path('activate/<uidb64>/<token>/', ActivateAccount.as_view(), name='activate'),
    path("login/", LoginView.as_view() , name="login"),  
    path("logout/", LogoutView.as_view(), name="logout"),

    path("profile", ProfileView.as_view(), name="profile"),
    path("change-password", ChangePasswordView.as_view(), name="change-password"),

    #reset password
    path("reset-password/", auth_views.PasswordResetView.as_view( template_name="accounts/password_reset.html"), name="password_reset"),
    path("reset-password/done/", auth_views.PasswordResetDoneView.as_view( template_name="accounts/password_reset_done.html"), name="password_reset_done"),
    path("reset-password-confirm/<uidb64>/<token>", auth_views.PasswordResetConfirmView.as_view( template_name="accounts/password_reset_confirm.html"), name="password_reset_confirm"),
    path("password-reset-complete/", auth_views.PasswordResetCompleteView.as_view( template_name="accounts/password_reset_complete.html"), name="password_reset_complete"),
    
    
    #manage users
    path('users/lists', views.UserListView.as_view(), name='list-users'),
    path('users/create', views.UserCreateView.as_view(), name='create-user'),
    path('users/<int:pk>/edit', views.UserUpdateView.as_view(), name='edit-user'),
    path('users/<int:pk>/delete', views.UserDeleteView.as_view(), name='delete-user'),
    
]