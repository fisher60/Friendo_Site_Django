from ariadne import MutationType
from .users import resolve_login

mutation = MutationType()
mutation.set_field("login", resolve_login)
