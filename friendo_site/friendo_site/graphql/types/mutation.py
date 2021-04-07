from ariadne import MutationType
from .users import resolve_login, get_user
from .servers import get_server

mutation = MutationType()
mutation.set_field("login", resolve_login)
mutation.set_field("user", get_user)
mutation.set_field("server", get_server)
