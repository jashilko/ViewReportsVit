from base import BaseDAO
from users.models import SiteUser


class UsersDAO(BaseDAO):
    model = SiteUser