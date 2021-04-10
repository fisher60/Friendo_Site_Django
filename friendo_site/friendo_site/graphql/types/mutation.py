from ariadne import MutationType
from .users import resolve_login, get_user
from .guilds import get_guild, modify_guild

mutation = MutationType()
mutation.set_field("login", resolve_login)
mutation.set_field("user", get_user)
mutation.set_field("get_guild", get_guild)
mutation.set_field("modify_guild", modify_guild)
