from ariadne import MutationType
from .users import (
    resolve_login,
    get_user,
    modify_user,
    get_user_watchlists,
    modify_user_watchlist,
    create_user_watchlist,
    get_user_watchlist_from_id,
    delete_user_watchlist_from_id,
)
from .guilds import get_guild, modify_guild

mutation = MutationType()
mutation.set_field("login", resolve_login)
mutation.set_field("user", get_user)
mutation.set_field("get_guild", get_guild)
mutation.set_field("modify_guild", modify_guild)
mutation.set_field("modify_user", modify_user)
mutation.set_field("get_user_watchlists", get_user_watchlists)
mutation.set_field("modify_user_watchlist", modify_user_watchlist)
mutation.set_field("get_watchlist_from_id", get_user_watchlist_from_id)
mutation.set_field("delete_watchlist_from_id", delete_user_watchlist_from_id)
mutation.set_field("create_watchlist", create_user_watchlist)
