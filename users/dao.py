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

    def all_operator_by_teamleader(cls):
        with session_maker() as session:
            query = select(SiteUser.phone_number).where(SiteUser.phone_teamleader == cls['oper'])
            result = session.execute(query)
            opers_info = result.scalars().all()

            # Преобразуйте данные  в словари
            opers_data = []
            for oper_phone in opers_info:
                opers_data.append(oper_phone)
            return opers_data


class UsersManDAO(BaseDAO):
    model = userman_users