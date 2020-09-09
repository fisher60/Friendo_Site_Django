from ariadne import QueryType
from friendo_site.users.models import User

query = QueryType()


@query.field("allUsers")
def resolve_all_users(root, info):
    return User.objects.all()
