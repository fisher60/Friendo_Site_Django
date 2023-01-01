from ariadne import QueryType
from friendo_site.users.models import User, token_required

query = QueryType()


@query.field("allUsers")
@token_required
def resolve_all_users(*_):
    return User.objects.all()
