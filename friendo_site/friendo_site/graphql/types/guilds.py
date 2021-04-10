from friendo_site.users.models import token_required
from friendo_site.guilds.models import Guild


@token_required
def get_guild(_, info, data):
    if data.get("guild_id", None):
        return Guild.objects.get(guild_id=data.get("guild_id", None))
    else:
        raise KeyError("guild_id is missing")


@token_required
def modify_guild(_, info, data):
    if guild_id := data.get("guild_id", None):
        this_guild, _ = Guild.objects.get_or_create(guild_id=guild_id)

        if doge_id := data.get("dogeboard_id", None):
            this_guild.dogeboard_id = int(doge_id)
        if doge_emoji := data.get("dogeboard_emoji", None):
            this_guild.dogeboard_emoji = doge_emoji
        if reactions_req := data.get("dogeboard_reactions_required", None):
            this_guild.dogeboard_reactions_required = int(reactions_req)

        this_guild.save()
        return this_guild

    else:
        raise KeyError("guild_id is missing")
