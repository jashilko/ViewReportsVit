from fastapi import APIRouter, Depends
from reports.dao import CdrDAO
from reports.schemas import SCRD
from reports.rb import RBCdr

router = APIRouter(prefix='/reports', tags=['Отчеты'])

@router.get("/", summary="Получить все записи", response_model=list[SCRD])
def get_all_cdr(request_body: RBCdr = Depends()) -> list[SCRD]:
    return CdrDAO.find_all(**request_body.to_dict())