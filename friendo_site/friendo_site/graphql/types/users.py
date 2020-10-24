from ariadne import ObjectType
from django.contrib.auth import authenticate, login
from friendo_site.users.models import User, token_required

user = ObjectType("User")


def generate_user_auth_token(user=None):
    if user is None:
        raise ValueError("User cannot be None.")
    return user.generate_token()


@token_required
def get_user(_, info, data):
    if data["discord_id"]:
        return User.objects.get(discord_id=data["discord_id"])
    elif data["username"]:
        return User.objects.get(username=data["username"])
    else:
        raise KeyError("discord_id or username invalid or both are missing")


def resolve_login(_, info, data):
    request = info.context["request"]
    user = authenticate(username=data["username"], password=data["password"])

    if user is None:
        return {"status": False, "error": "Invalid username or password", "user": None}

    # User is valid
    login(request, user)

    auth_token = generate_user_auth_token(user)
    return {"status": True, "token": str(auth_token.token)}
