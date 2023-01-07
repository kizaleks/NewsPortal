from django.contrib import admin
from django.urls import path
from django.urls import include
from django.contrib.auth.views import LoginView, LogoutView
from .views import BaseRegisterView

from django.urls import path
from .views import SignUp

urlpatterns = [
    path("", include("allauth.urls")),
    ]