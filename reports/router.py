import datetime

from fastapi import APIRouter, Depends
from reports.dao import CdrDAO
from reports.schemas import SCRD
from reports.rb import RBCdr
from users.dependencies import get_current_user
from users.schemas import SUserAuth

router = APIRouter(prefix='/reports', tags=['Отчеты'])

@router.get("/", summary="Получить все записи", response_model=list[SCRD])
def get_all_cdr(request_body: RBCdr = Depends(), user_data: SUserAuth = Depends(get_current_user)) -> list[SCRD]:
    return CdrDAO.find_cdr(RBCdr)

@router.get("/by_operator", summary="Записи одного оператора", response_model=list[SCRD])
def get_all_calls_by_oper(request_body: RBCdr = Depends(), user_data: SUserAuth = Depends(get_current_user)) -> list[SCRD]:
    # Если пользователь не указан в запросе, делаем запрос по залогиненному
    if 'oper' in request_body.to_dict():
        pass
    else:
        request_body.oper = user_data.phone_number
    if 'date_from' in request_body.to_dict():
        pass
    else:
        request_body.date_from = str(datetime.datetime.today() - datetime.timedelta(30))
    return {'req': request_body.to_dict(), 'res': CdrDAO.find_cdr_byoper(request_body.to_dict())}