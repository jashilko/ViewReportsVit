from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
from database import session_maker

class BaseDAO:
    model = None
    @classmethod
    async def find_all(cls, **filter_by):
        async with session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return list(result.scalars())


    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def add(cls, **values):
        async with session_maker() as session:
            new_instance = cls.model(**values)
            session.add(new_instance)
            try:
                await session.commit()
            except SQLAlchemyError as e:
                await session.rollback()
                raise e
            return new_instance

    @classmethod
    async def update(cls, id: int, **values):
        """
        Общий метод для обновления записей
        :param id: ID записи для обновления
        :param values: Поля и их новые значения
        :return: Обновленный объект
        """
        async with session_maker() as session:
            try:
                instance = await cls.find_one_or_none(id=id)
                if not instance:
                    raise ValueError(f"Объект с ID {id} не найден")

                for key, value in values.items():
                    setattr(instance, key, value)

                session.add(instance)
                await session.flush()  # Применяем изменения
                await session.commit()  # Фиксируем в БД
                return instance
            except Exception as e:
                await session.rollback()
                raise e