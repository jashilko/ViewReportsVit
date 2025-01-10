from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates

from users.router import get_all_teamleader

# router = APIRouter(prefix='/', tags=['Фронтенд'])
# templates = Jinja2Templates(directory="public")
#
# @router.get("/register", summary="Registration Form", tags=['WebPages'])
# def login(request: Request, team_leaders=Depends(get_all_teamleader)):
#     return templates.TemplateResponse(name='register.html', context={"request": request,
#                                                                       "group_leader_phones": team_leaders})

# @router.get('/calls/{id}')
# def get_calls_one_oper_html(request: Request, Depends = Depends()):
#     return templates.TemplateResponse(name="index.html", context={'request': request, 'reports1': reports})
#
# @router.get('/students')
# async def get_students_html(request: Request):
#     return templates.TemplateResponse(name='students.html', context={'request': request})
#
# @router.get("/")
# def main(request: Request, reports=Depends(get_all_cdr)):
#     return templates.TemplateResponse(name="index.html", context={'request': request, 'reports1': reports})