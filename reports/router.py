from fastapi import APIRouter
from reports.dao import CdrDAO
from reports.schemas import SCRD

router = APIRouter(prefix='/reports', tags=['Отчеты'])

@router.get("/", summary="Получить все записи", response_model=list[SCRD])
def get_all_cdr():
    return CdrDAO.find_all()