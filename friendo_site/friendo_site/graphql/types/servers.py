from friendo_site.users.models import token_required
from friendo_site.servers.models import Server


@token_required
def get_server(_, info, data):
    if data.get("guild_id", None):
        return Server.objects.get(guild_id=data.get("guild_id", None))
    else:
        raise KeyError("guild_id is missing")


@token_required
def create_server(_, info, data):
    if data.get("guild_id", None):
        new_server = Server(guild_id=int(data.get("guild_id")))
        new_server.save()
        return new_server
    else:
        raise KeyError("guild_id is missing")


@token_required
def update_server(_, info, data):
    if data.get("guild_id", None):
        this_server = Server.objects.get(guild_id=data.get("guild_id", None))
        if data.get("dogeboard_id", None):
            this_server.dogeboard_id = int(data.get("dogeboard_id", None))
        if data.get("dogeboard_emoji", None):
            this_server.dogeboard_emoji = data.get("dogeboard_emoji", None)
        if data.get("dogeboard_reactions_required", None):
            this_server.dogeboard_reaction_required = int(
                data.get("dogeboard_reactions_required", None)
            )

        this_server.save()
        return this_server

    else:
        raise KeyError("guild_id is missing")
