from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

app_name = 'account'

urlpatterns = [
    path("register/", UserCreateView.as_view(), name="register"),
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]
