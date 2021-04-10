from friendo_site.users.models import token_required
from friendo_site.guilds.models import Guild


@token_required
def get_guild(_, info, data):
    if data.get("guild_id", None):
        return Guild.objects.get(guild_id=data.get("guild_id", None))
    else:
        raise KeyError("guild_id is missing")


@token_required
def create_guild(_, info, data):
    if data.get("guild_id", None):
        new_guild = Guild(guild_id=int(data.get("guild_id")))
        new_guild.save()
        return new_guild
    else:
        raise KeyError("guild_id is missing")


@token_required
def update_guild(_, info, data):
    if data.get("guild_id", None):
        this_guild = Guild.objects.get(guild_id=data.get("guild_id", None))
        if data.get("dogeboard_id", None):
            this_guild.dogeboard_id = int(data.get("dogeboard_id", None))
        if data.get("dogeboard_emoji", None):
            this_guild.dogeboard_emoji = data.get("dogeboard_emoji", None)
        if data.get("dogeboard_reactions_required", None):
            this_guild.dogeboard_reaction_required = int(
                data.get("dogeboard_reactions_required", None)
            )

        this_guild.save()
        return this_guild

    else:
        raise KeyError("guild_id is missing")
