from reports.model import CDR
from base import BaseDAO
from sqlalchemy.future import select
from database import session_maker

class CdrDAO(BaseDAO):
    model = CDR

    @classmethod
    def find_cdr(cls):
        with session_maker() as session:
            query = select(cls.model).limit(100)
            result = session.execute(query)
            cdr_info = result.scalars().all()

            # Преобразуйте данные  в словари
            cdr_data = []
            for cdr in cdr_info:
                student_dict = cdr.to_dict()
                cdr_data.append(student_dict)

            return cdr_data
