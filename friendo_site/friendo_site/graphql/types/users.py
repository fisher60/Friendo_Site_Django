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


@token_required
def modify_user(_, info, data):
    if discord_user_id := data.get("discord_id", None):
        this_user, user_was_created = User.objects.get_or_create(
            discord_id=discord_user_id
        )

        if user_was_created:
            this_user.username = f"temp_{discord_user_id}"

        if timezone_data := data.get("timezone_name", None):
            this_user.timezone_name = timezone_data

        this_user.save()
        return this_user
    else:
        raise KeyError("discord_id is a required parameter.")


def resolve_login(_, info, data):
    request = info.context["request"]
    user = authenticate(username=data["username"], password=data["password"])

    if user is None:
        return {"status": False, "error": "Invalid username or password", "user": None}

    # User is valid
    login(request, user)

    auth_token = generate_user_auth_token(user)
    return {"status": True, "token": str(auth_token.token)}
