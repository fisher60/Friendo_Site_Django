from ariadne import ObjectType
from django.contrib.auth import authenticate, login

user = ObjectType("User")


def generate_user_auth_token(user=None):
    if user is None:
        raise ValueError("User cannot be None.")
    return user.generate_token()


def resolve_login(_, info, data):
    request = info.context["request"]
    user = authenticate(username=data["username"], password=data["password"])

    if user is None:
        return {"status": False, "error": "Invalid username or password", "user": None}

    # User is valid
    login(request, user)

    auth_token = generate_user_auth_token(user)
    return {"status": True, "token": str(auth_token.token)}
