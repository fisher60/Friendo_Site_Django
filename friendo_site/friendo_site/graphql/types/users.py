from ariadne import ObjectType
from django.contrib.auth import authenticate, login
from friendo_site.users.models import User, token_required, WatchList

user_type = ObjectType("User")

watchlist_object = ObjectType("WatchList")


def generate_user_auth_token(user=None):
    if user is None:
        raise ValueError("User cannot be None.")
    return user.generate_token()


@watchlist_object.field("owners")
def resolve_watchlist_owners_field(obj, _):
    return obj.owners.all()


@watchlist_object.field("titles")
def resolve_watchlist_titles_field(obj, _):
    return obj.watchlisttitle_set.all()


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
        return User.objects.get(discord_id=discord_id).watchlist_set.all()
    else:
        raise KeyError("discord_id missing or invalid.")


@token_required
def create_user_watchlist(_, info, data):
    watchlist_name = data.get("watchlist_name")
    owner_discord_id = data.get("owner_discord_id")

    owner = User.objects.get(discord_id=owner_discord_id)
    new_watchlist = WatchList.objects.create(name=watchlist_name)
    new_watchlist.save()
    new_watchlist.owners.add(owner)

    return new_watchlist


@token_required
def modify_user_watchlist(_, info, data):
    watchlist_id = data.get("watch_list_id")
    this_watch_list = WatchList.objects.get(id=watchlist_id)
    if change_name := data.get("change_name"):
        this_watch_list.name = change_name
    if remove_user := data.get("remove_user_discord_id"):
        this_watch_list.owners.remove(User.objects.get(discord_id=remove_user))
    this_watch_list.save()

    return this_watch_list


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
            this_user.set_unusable_password()

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
        return {
            "status": False,
            "error": "Invalid username or password",
            "user": None,
        }

    # User is valid
    login(request, user)

    auth_token = generate_user_auth_token(user)
    return {"status": True, "token": str(auth_token.token)}
