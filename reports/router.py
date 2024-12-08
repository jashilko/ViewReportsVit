from fastapi import APIRouter
from sqlalchemy import select
from database import session_maker
from reports.model import CDR

router = APIRouter(prefix='/reports', tags=['Отчеты'])

@router.get("/", summary="Получить все записи")
async def get_all_students():
    with session_maker() as session:
        query = select(CDR).limit(100)
        result = session.execute(query)
        all_cdr = result.scalars().all()
        return all_cdr