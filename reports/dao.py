from reports.model import CDR
from base import BaseDAO
from sqlalchemy.future import select
from database import session_maker
from sqlalchemy import and_, or_, func, case, desc, literal_column
from reports.model import CDR
from users.router import UsersNameDAO

class CdrDAO(BaseDAO):
    model = CDR

    async def find_cdr_byoper(conditions):
        async with (session_maker() as session):
            query = select(CDR).where(CDR.calldate >= conditions['date_from'] if 'date_from' in conditions else 1==1,
                                      CDR.calldate <= conditions['date_to'] if 'date_to' in conditions else 1==1,
                                      or_(CDR.src == conditions['oper'], CDR.dst == conditions['oper']) if 'oper' in conditions else 1==1
                                      ).order_by(desc(CDR.calldate))
            result = await session.execute(query)
            cdr_info = result.scalars().fetchall()

            # Преобразуйте данные  в словари
            cdr_data = []
            for cdr in cdr_info:
                student_dict = cdr.to_dict()
                cdr_data.append(student_dict)

            return cdr_data

    # Получить статистику по одному оператору
    async def get_one_oper_stat(cls):
        async with session_maker() as session:
            results = await session.execute(
                select(
                    func.count().label("total_calls"),
                    func.sum(case((CDR.dst == cls['oper'], 1), else_=0)).label("incoming_calls"),
                    func.sum(case((CDR.src == cls['oper'], 1), else_=0)).label("outgoing_calls"),
                    func.sum(CDR.billsec).label("total_duration"),
                    func.avg(CDR.billsec).label("average_duration"),
                    func.sum(case((CDR.dst == cls['oper'], CDR.billsec), else_=0)).label("total_incoming_duration"),
                    func.avg(case((CDR.dst == cls['oper'], CDR.billsec), else_=literal_column("NULL"))).label(
                        "average_incoming_duration"),
                    func.sum(case((CDR.src == cls['oper'], CDR.billsec), else_=0)).label("total_outgoing_duration"),
                    func.avg(case((CDR.src == cls['oper'], CDR.billsec), else_=literal_column("NULL"))).label("average_outgoing_duration")
                ).filter(
                    (CDR.src == cls['oper']) | (CDR.dst == cls['oper']),
                    CDR.calldate >= cls['date_from'] if 'date_from' in cls else True,
                    CDR.calldate <= cls['date_to'] if 'date_to' in cls else True
                )
            )
            results = results.first()
        return {
            'phone_number': cls['oper'],
            'oper_name': await UsersNameDAO.user_name(cls['oper']),
            'total_calls': results.total_calls,
            'incoming_calls': results.incoming_calls if results.incoming_calls else 0,
            'outgoing_calls': results.outgoing_calls if results.outgoing_calls else 0,
            'total_duration': results.total_duration if results.total_duration else 0,
            'average_duration': results.average_duration if results.average_duration else 0,
            'total_incoming_duration': results.total_incoming_duration if results.total_incoming_duration else 0,
            'average_incoming_duration': results.average_incoming_duration if results.average_incoming_duration else 0,
            'total_outgoing_duration': results.total_outgoing_duration if results.total_outgoing_duration else 0,
            'average_outgoing_duration': results.average_outgoing_duration if results.average_outgoing_duration else 0
        }

