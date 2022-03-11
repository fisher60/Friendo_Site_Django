from typing import Optional

from ariadne import ObjectType
from django.contrib.auth import authenticate, login
from friendo_site.users.models import User, token_required, WatchList

user_type = ObjectType("User")

watchlist_object = ObjectType("WatchList")


def generate_user_auth_token(user=None):
    if user is None:
        raise ValueError("User cannot be None.")
    return user.generate_token()


def get_or_create_user_from_id(discord_id: int) -> User:
    this_user, user_was_created = User.objects.get_or_create(
        discord_id=discord_id
    )

    if user_was_created:
        this_user.username = f"temp_{discord_id}"
        this_user.set_unusable_password()

    this_user.save()

    return this_user


@watchlist_object.field("maintainers")
def resolve_watchlist_maintainers_field(obj, _):
    return obj.maintainers.all()


@watchlist_object.field("titles")
def resolve_watchlist_titles_field(obj, _):
    return obj.watchlisttitle_set.all()


@user_type.field("watchlists")
def resolve_watchlist(obj, _):
    return obj.owned_watchlists.all()


@token_required
def get_user_watchlist_from_id(_, info, data):
    return WatchList.objects.get(id=int(data.get("watch_list_id")))


@token_required
def delete_user_watchlist_from_id(_, info, data) -> bool:
    """
    Attempt to get and delete a WatchList entry.

    Returns whether the number of deleted entries is greater than 0.
    """
    deleted_objects = WatchList.objects.get(id=int(data.get("watch_list_id"))).delete()
    return deleted_objects[0] > 0


@token_required
def get_user_watchlists(_, info, data):
    if discord_id := data.get("discord_id"):
        return User.objects.get(discord_id=discord_id).owned_watchlists.all()
    else:
        raise KeyError("discord_id missing or invalid.")


@token_required
def create_user_watchlist(_, info, data):
    watchlist_name = data.get("watchlist_name")
    owner_discord_id = data.get("owner_discord_id")
    owner = get_or_create_user_from_id(owner_discord_id)

    new_watchlist = WatchList.objects.create(name=watchlist_name, owner=owner)
    new_watchlist.save()

    return new_watchlist


@token_required
def modify_user_watchlist(_, info, data):
    watchlist_id = data.get("watch_list_id")
    this_watch_list = WatchList.objects.get(id=watchlist_id)

    if change_name := data.get("change_name"):
        this_watch_list.name = change_name
    if remove_user := data.get("remove_user_discord_id"):
        this_watch_list.maintainers.remove(User.objects.get(discord_id=remove_user))
    if add_user := data.get("add_user_discord_id"):
        user_to_add = get_or_create_user_from_id(add_user)
        this_watch_list.maintainers.add(user_to_add)

    this_watch_list.save()

    return this_watch_list


@token_required
def get_user(_, info, data):
    if data["discord_id"]:
        return User.objects.get(discord_id=data["discord_id"])
    else:
        raise KeyError("discord_id invalid or missing")


@token_required
def modify_user(_, info, data):
    if discord_user_id := data.get("discord_id"):
        this_user = get_or_create_user_from_id(discord_user_id)

        if timezone_data := data.get("timezone_name"):
            this_user.timezone_name = timezone_data

        this_user.save()
        return this_user
    else:
        raise KeyError("discord_id is a required parameter.")


def resolve_login(_, info, data):
    request = info.context["request"]
    user = authenticate(username=data["username"], password=data["password"])

    if user is None:
        return {
            "status": False,
            "error": "Invalid username or password",
            "user": None,
        }

    # User is valid
    login(request, user)

    auth_token = generate_user_auth_token(user)
    return {"status": True, "token": str(auth_token.token)}
