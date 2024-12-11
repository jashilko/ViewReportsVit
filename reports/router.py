from fastapi import APIRouter, Depends
from reports.dao import CdrDAO
from reports.schemas import SCRD
from reports.rb import RBCdr
from users.dependencies import get_current_admin_user
from users.schemas import SUserAuth

router = APIRouter(prefix='/reports', tags=['Отчеты'])

@router.get("/", summary="Получить все записи", response_model=list[SCRD])
def get_all_cdr(request_body: RBCdr = Depends(), user_data: SUserAuth = Depends(get_current_admin_user)) -> list[SCRD]:
    return CdrDAO.find_all(**request_body.to_dict())