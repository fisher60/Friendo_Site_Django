from django.urls import path

from .views import discord_login, discord_login_redirect, login_view, register

urlpatterns = [
    path("discord-auth/", discord_login, name="discord-auth"),
    path("login/", login_view, name="login"),
    path("register/", register, name="register"),
    path("auth_redirect", discord_login_redirect, name="auth_redirect"),
]
