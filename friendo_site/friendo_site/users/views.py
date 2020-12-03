import requests

from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.conf import settings
from django.db import IntegrityError
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import UserRegisterForm


def discord_login(request: HttpRequest):
    return redirect(settings.DISCORD_AUTH_URL)


@login_required
def discord_login_redirect(request: HttpRequest):
    code = request.GET.get("code")
    user_data = exchange_code(code)

    try:
        user = request.user
        user.discord_id = user_data.get("id")
        user.discord_username = user_data.get("username")
        user.discord_discriminator = user_data.get("discriminator")
        user.is_bot = user_data.get("bot", False)
        user.discord_avatar = user_data.get("avatar")
        try:
            user.save()
        except IntegrityError:
            messages.error(request, "Discord user already belongs to account")
            return redirect("profile")

        messages.success(request, "Discord account verified")
    except KeyError:
        messages.error(request, "Could not retrieve user data")

    return redirect("profile")


def exchange_code(code: str) -> dict:
    data = {
        "client_id": settings.BOT_CLIENT_ID,
        "client_secret": settings.BOT_CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": f"http://{settings.HOST_DNS}{reverse('auth_redirect')}",
        "scope": "identify",
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(settings.DISCORD_TOKEN_URL, data=data, headers=headers)
    credentials = response.json()

    if "access_token" in credentials:
        access_token = credentials["access_token"]
        response = requests.get(
            settings.DISCORD_USER_URL,
            headers={"Authorization": f"Bearer {access_token}"},
        )
        user = response.json()
        return user
    else:
        return credentials


def register(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = UserRegisterForm(request.POST)

            if form.is_valid():
                form.save()
                return redirect("login")
        else:
            form = UserRegisterForm()
    else:
        messages.error(request, "You must logout to register a new account")
        return redirect("profile")

    return render(request, "users/register.html", {"form": form})


def login_view(request):
    if not request.user.is_authenticated:
        username = request.POST.get("username", None)
        password = request.POST.get("password", None)
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
        else:
            return render(request, "users/login.html")

    return redirect("profile")


@login_required
def profile(request):
    return render(request, "users/profile.html")


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "You have been logged out.")
    return redirect("index")
