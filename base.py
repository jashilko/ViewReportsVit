from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
from database import session_maker

class BaseDAO:
    model = None
    @classmethod
    def find_all(cls, **filter_by):
        with session_maker() as session:
            query = select(cls.model).filter_by(**filter_by).limit(100)
            result = session.execute(query)
            return result.scalars().all()

    @classmethod
    def find_one_or_none(cls, **filter_by):
        with session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    def add(cls, **values):
        with session_maker() as session:
            with session.begin():
                new_instance = cls.model(**values)
                session.add(new_instance)
                try:
                    session.commit()
                except SQLAlchemyError as e:
                    session.rollback()
                    raise e
                return new_instance