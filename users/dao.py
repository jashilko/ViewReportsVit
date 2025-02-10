from sqlalchemy import distinct, update

from base import BaseDAO
from users.models import SiteUser, userman_users, users
from database import session_maker, session_maker_asterisk
from sqlalchemy.future import select


class UsersDAO(BaseDAO):
    model = SiteUser

    @classmethod
    def update_password(cls, phone_num: str, new_pass: str):
        with session_maker() as session:  # Использование контекста для сессии
            try:
                # Находим пользователя с указанным номером телефона
                user = session.query(SiteUser).filter_by(phone_number=phone_num).first()
                if not user:
                    raise ValueError(f"Пользователь с номером {phone_num} не найден.")

                # Обновляем пароль пользователя
                user.password = new_pass  # Прямое изменение свойства
                session.commit()  # Сохраняем изменения
            except Exception as e:
                session.rollback()  # Откатываем изменения в случае ошибки
                raise e


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

    @classmethod
    def update_leader(cls, phone_number, new_leader):
        with session_maker() as session:  # Использование контекста для сессии
            try:
                # Находим пользователя с указанным номером телефона
                user = session.query(SiteUser).filter_by(phone_number=phone_number).first()
                if not user:
                    raise ValueError(f"Пользователь с номером {phone_number} не найден.")

                # Обновляем лидера пользователя
                user.phone_teamleader = new_leader  # Прямое изменение свойства
                session.commit()  # Сохраняем изменения
            except Exception as e:
                session.rollback()  # Откатываем изменения в случае ошибки
                raise e

    @classmethod
    def update_roles(cls, phone_number, roles):
        with session_maker() as session:  # Использование контекста для сессии
            try:
                # Находим пользователя с указанным номером телефона
                user = session.query(SiteUser).filter_by(phone_number=phone_number).first()
                if not user:
                    raise ValueError(f"Пользователь с номером {phone_number} не найден.")

                # Обновляем роли пользователя
                user.is_operator = True if "Оператор" in roles else False
                user.is_teamlead = True if "Руководитель" in roles else False
                user.is_controller = True if "Контроллер" in roles else False
                session.commit()  # Сохраняем изменения
            except Exception as e:
                session.rollback()  # Откатываем изменения в случае ошибки
                raise e


class UsersManDAO(BaseDAO):
    model = userman_users

    @classmethod
    def all_operator_list(cls):
        with session_maker() as session:
            # Создаем запрос с distinct
            query = select(distinct(userman_users.username))

            # Выполняем запрос
            result = session.execute(query).scalars().all()

            # Преобразуем данные в список
            opers_list = [oper_phone for oper_phone in result]
            return opers_list

class UsersNameDAO(BaseDAO):
    model = users

    @classmethod
    def all_operator_list(cls):
        with session_maker() as session:
            # Создаем запрос с distinct
            query = select(users.extension, users.name)

            # Выполняем запрос
            result = session.execute(query).all()

            # Преобразуем данные в список
            opers_dict = {extension: name for extension, name in result}
            return opers_dict
    @classmethod

    def user_name(cls, phone_number):
        with session_maker() as session:
            # Создаем запрос с distinct
            query = select(users.name).where(users.extension == phone_number)

            # Выполняем запрос
            result = session.execute(query).first()

            return result[0] if result else None