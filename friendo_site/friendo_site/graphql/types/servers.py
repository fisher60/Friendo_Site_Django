from friendo_site.users.models import token_required
from friendo_site.servers.models import Server


@token_required
def get_server(_, info, data):
    if data.get("server_id", None):
        return Server.objects.get(server_id=data.get("server_id", None))
    else:
        raise KeyError("server_id is missing")
