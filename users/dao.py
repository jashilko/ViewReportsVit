from sqlalchemy import distinct, update

from base import BaseDAO
from users.models import SiteUser, users
from database import session_maker, session_maker_asterisk
from sqlalchemy.future import select


class UsersDAO(BaseDAO):
    model = SiteUser

    @classmethod
    async def update_by_phone(cls, phone_number: str, **updates):
        """Универсальный метод обновления по номеру телефона"""
        user = await cls.find_one_or_none(phone_number=phone_number)
        if not user:
            raise ValueError(f"Пользователь с номером {phone_number} не найден")
        return await cls.update(user.id, **updates)

class UsersNameDAO(BaseDAO):
    model = users

    @classmethod
    async def all_operator_list(cls):
        async with session_maker_asterisk() as session:
            # Создаем запрос с distinct
            query = select(users.extension, users.name)

            # Выполняем запрос
            result = await session.execute(query)
            all_oper_list = result.all()
            # Преобразуем данные в список
            opers_dict = {extension: name for extension, name in all_oper_list}
            return opers_dict

    @classmethod
    async def user_name(cls, phone_number):
        session = session_maker_asterisk()
        try:
            query = select(users.name).where(users.extension == phone_number).limit(1)
            result = await session.execute(query)
            return result.scalar_one_or_none()
        finally:
            await session.close()

    @classmethod
    async def all_operator_phone(cls):
        async with session_maker_asterisk() as session:
            # Создаем запрос с distinct
            query = select(distinct(users.extension))

            # Выполняем запрос
            result = await session.execute(query)
            all_oper_info = result.scalars().all()
            # Преобразуем данные в список
            opers_list = [oper_phone for oper_phone in all_oper_info]
            return opers_list
