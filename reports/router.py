import datetime

from fastapi import APIRouter, Depends
from reports.dao import CdrDAO
from reports.schemas import SCRD
from reports.rb import RBCdr
from users.dao import UsersDAO
from users.dependencies import get_current_user
from users.schemas import SUserAuth

router = APIRouter(prefix='/reports', tags=['Отчеты'])

@router.get("/", summary="Получить все записи", response_model=list[SCRD])
def get_all_cdr(request_body: RBCdr = Depends(), user_data: SUserAuth = Depends(get_current_user)) -> list[SCRD]:
    return CdrDAO.find_cdr(RBCdr)

@router.get("/by_operator", summary="Записи одного оператора", response_model=list[SCRD])
def get_all_calls_by_oper(request_body: RBCdr = Depends(), user_data = Depends(get_current_user)) -> list[SCRD]:
    # Если пользователь не указан в запросе, делаем запрос по залогиненному
    print(request_body.to_dict())
    if 'oper' in request_body.to_dict():
        if (request_body.to_dict()['oper'] != user_data.phone_number
                and not request_body.to_dict()['oper'] in UsersDAO.all_operator_by_teamleader({'oper': user_data.phone_number})):
            return {'req': request_body.to_dict(), 'res': {}, 'warning': 'Нет прав на просмотр звонков выбранного оператора'}
    else:
        request_body.oper = user_data.phone_number
    if 'date_from' in request_body.to_dict():
        pass
    else:
        request_body.date_from = str(datetime.datetime.today() - datetime.timedelta(30))
    return {'req': request_body.to_dict(), 'res': CdrDAO.find_cdr_byoper(request_body.to_dict()), 'warning': ""}

@router.get("/oper_stat", summary="Статистика оператора")
def get_one_oper_stat(request_body: RBCdr = Depends()):
    return CdrDAO.get_one_oper_stat(request_body.to_dict())

@router.get("/group_oper_stat", summary="Статистика операторов группы")
def get_group_oper_stat(request_body: RBCdr = Depends(), user_data = Depends(get_current_user)):
    # Список операторов
    if not user_data.is_teamlead:
        return {'req': request_body.to_dict(), 'res': [], 'warning': "Нет прав на просмотр статистики группы"}

    if not 'oper' in request_body.to_dict():
        request_body.oper = user_data.phone_number

    if 'date_from' in request_body.to_dict():
        pass
    else:
        request_body.date_from = str(datetime.datetime.today() - datetime.timedelta(30))

    users_list = UsersDAO.all_operator_by_teamleader(request_body.to_dict())



    # Цикл по каждому
    users_dict = []
    for user in users_list:
        one_user = RBCdr(oper=user,
                         date_from=request_body.to_dict()['date_from'] if 'date_from' in request_body.to_dict() else None,
                         date_to=request_body.to_dict()['date_to'] if 'date_to' in request_body.to_dict() else None)
        user_stat = get_one_oper_stat(one_user)
        users_dict.append(user_stat)
    return {'req': request_body.to_dict(), 'res': users_dict, 'warning': ""}