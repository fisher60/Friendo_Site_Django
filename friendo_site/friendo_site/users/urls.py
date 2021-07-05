from django.urls import path

from .views import discord_login, discord_login_redirect

urlpatterns = [
    path("login/", discord_login, name="login"),
    path("auth_redirect", discord_login_redirect, name="auth_redirect"),
]
