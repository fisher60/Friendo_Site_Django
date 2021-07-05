import requests

from django.http import HttpRequest, JsonResponse
from django.shortcuts import redirect, render
from django.conf import settings
from django.urls import reverse
from django.contrib.auth import authenticate, login

from .forms import UserRegisterForm


def discord_login(request: HttpRequest):
    return redirect(settings.DISCORD_AUTH_URL)


def discord_login_redirect(request: HttpRequest):
    code = request.GET.get("code")
    user = exchange_code(code)
    return JsonResponse({"User": user})


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
    if request.method == "POST":
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserRegisterForm()

    return render(request, "users/register.html", {"form": form})


def login_view(request):
    username = request.POST.get("username", None)
    password = request.POST.get("password", None)
    user = authenticate(request, username=username, password=password)
    if user:
        login(request, user)
        return redirect("index")
    else:
        return render(request, "users/login.html")
