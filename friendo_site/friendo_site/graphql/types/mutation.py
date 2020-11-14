from ariadne import MutationType
from .users import resolve_login, get_user

mutation = MutationType()
mutation.set_field("login", resolve_login)
mutation.set_field("user", get_user)
