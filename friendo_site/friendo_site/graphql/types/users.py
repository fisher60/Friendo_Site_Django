from ariadne import ObjectType
from django.contrib.auth import authenticate, login
from friendo_site.users.models import AuthToken, User

user = ObjectType("User")


def generate_user_auth_token(user=None):
    if user is None:
        raise ValueError("User cannot be None.")

    auth_token = AuthToken(user=user)
    auth_token.set_expiration()
    auth_token.encode_token()
    auth_token.save()
    return auth_token


def resolve_login(_, info, data):
    request = info.context["request"]
    user = authenticate(username=data["username"], password=data["password"])

    if user is None:
        return {"status": False, "error": "Invalid username or password", "user": None}

    # User is valid
    login(request, user)

    auth_token = generate_user_auth_token(user)
    return {"status": True, "token": str(auth_token.token)}
