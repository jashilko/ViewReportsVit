from sqlalchemy import distinct, update

from base import BaseDAO
from users.models import SiteUser, users
from database import session_maker, session_maker_asterisk
from sqlalchemy.future import select


class UsersDAO(BaseDAO):
    model = SiteUser

    @classmethod
    async def update_password(cls, phone_num: str, new_pass: str):
        async with session_maker() as session:  # Использование контекста для сессии
            try:
                # Находим пользователя с указанным номером телефона
                user = await cls.find_one_or_none(phone_number=phone_num)
                if not user:
                    raise ValueError(f"Пользователь с номером {phone_num} не найден.")

                # Обновляем пароль пользователя
                user.password = new_pass  # Прямое изменение свойства
                session.add(user)  # Добавляем в сессию
                await session.flush()  # Применяем изменения
                await session.commit()  # Фиксируем в БД
            except Exception as e:
                await session.rollback()  # Откатываем изменения в случае ошибки
                raise e

    @classmethod
    async def all_operator_by_teamleader(cls, phone_teamleader):
        async with session_maker() as session:
            opers_info = await cls.find_all(phone_teamleader=phone_teamleader)
            # Преобразуйте данные  в словари
            opers_data = []
            for oper_phone in opers_info:
                opers_data.append(oper_phone.phone_number)
            return opers_data

    @classmethod
    async def update_leader(cls, phone_number, new_leader):
        async with session_maker() as session:  # Использование контекста для сессии
            try:
                # Находим пользователя с указанным номером телефона
                user = await cls.find_one_or_none(phone_number=phone_number)
                if not user:
                    raise ValueError(f"Пользователь с номером {phone_number} не найден.")

                # Обновляем лидера пользователя
                user.phone_teamleader = new_leader  # Прямое изменение свойства
                session.add(user)  # Добавляем в сессию
                await session.flush()  # Применяем изменения
                await session.commit()  # Фиксируем в БД
            except Exception as e:
                await session.rollback()  # Откатываем изменения в случае ошибки
                raise e

    @classmethod
    async def update_roles(cls, phone_number, roles):
        async with session_maker() as session:  # Использование контекста для сессии
            try:
                # Находим пользователя с указанным номером телефона
                user = await cls.find_one_or_none(phone_number=phone_number)
                if not user:
                    raise ValueError(f"Пользователь с номером {phone_number} не найден.")

                # Обновляем роли пользователя
                user.is_operator = True if "Оператор" in roles else False
                user.is_teamlead = True if "Руководитель" in roles else False
                user.is_controller = True if "Контроллер" in roles else False
                session.add(user)  # Добавляем в сессию
                await session.flush()  # Применяем изменения
                await session.commit()  # Фиксируем в БД
            except Exception as e:
                await session.rollback()  # Откатываем изменения в случае ошибки
                raise e

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
