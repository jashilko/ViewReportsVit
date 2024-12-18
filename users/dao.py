from base import BaseDAO
from users.models import SiteUser, userman_users


class UsersDAO(BaseDAO):
    model = SiteUser

class UsersManDAO(BaseDAO):
    model = userman_users