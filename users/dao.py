from base import BaseDAO
from users.models import SiteUser, userman_users
from database import session_maker
from sqlalchemy.future import select


class UsersDAO(BaseDAO):
    model = SiteUser

    @classmethod
    def all_teamleader(cls):
        with session_maker() as session:
            query = select(SiteUser.phone_number).where(SiteUser.is_teamlead)
            result = session.execute(query)
            teamleader_info = result.scalars().all()

            # Преобразуйте данные  в словари
            teamleader_data = []
            for teamleader in teamleader_info:
                teamleader_data.append(teamleader)
            return teamleader_data

class UsersManDAO(BaseDAO):
    model = userman_users