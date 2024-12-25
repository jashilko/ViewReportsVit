from reports.model import CDR
from base import BaseDAO
from sqlalchemy.future import select
from database import session_maker
from sqlalchemy import and_, or_
from reports.model import CDR

class CdrDAO(BaseDAO):
    model = CDR
    @classmethod
    def find_cdr(cls):
        with session_maker() as session:
            query = select(CDR).limit(100)
            result = session.execute(query)
            cdr_info = result.scalars().all()

            # Преобразуйте данные  в словари
            cdr_data = []
            for cdr in cdr_info:
                student_dict = cdr.to_dict()
                cdr_data.append(student_dict)

            return cdr_data

    def find_cdr_byoper(conditions):
        with session_maker() as session:
            query = select(CDR).where(CDR.calldate >= conditions['date_from'] if 'date_from' in conditions else 1==1,
                                      CDR.calldate <= conditions['date_to'] if 'date_to' in conditions else 1==1,
                                      or_(CDR.src == conditions['oper'], CDR.dst == conditions['oper']) if 'oper' in conditions else 1==1).limit(100)
            result = session.execute(query)
            cdr_info = result.scalars().all()

            # Преобразуйте данные  в словари
            cdr_data = []
            for cdr in cdr_info:
                student_dict = cdr.to_dict()
                cdr_data.append(student_dict)

            return cdr_data