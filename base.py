from sqlalchemy.future import select
from database import session_maker

class BaseDAO:
    model = None
    @classmethod
    def find_all(cls):
        with session_maker() as session:
            query = select(cls.model).limit(100)
            result = session.execute(query)
            return result.scalars().all()