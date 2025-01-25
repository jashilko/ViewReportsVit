from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from reports.router import router as router_cdr
from users.router import router as router_users, get_all_users, register_admin
from reports.router import get_all_cdr, get_all_calls_by_oper, get_group_oper_stat
from users.router import get_me, get_all_teamleader
from database import create_table
from users.models import SiteUser
from config import get_pass
from  reports.statistic import Statistic


app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name='static')
app.mount(
    "/audio",  # URL-часть маршрута должна начинаться с "/"
    StaticFiles(directory='/audio', html=True),  # Абсолютный путь к папке с файлами
    name="audio"
)
templates = Jinja2Templates(directory="public")
app.include_router(router_cdr)
app.include_router(router_users)
# app = FastAPI(docs_url=get_api_url(), redoc_url=None)


#Создадим таблицу пользователей для первого входа
create_table(SiteUser)
register_admin(get_pass())

@app.get("/register", summary="Registration Form", tags=['WebPages'])
def login(request: Request, team_leaders=Depends(get_all_teamleader)):
    return templates.TemplateResponse(name='register.html', context={"request": request,
                                                                      "group_leader_phones": team_leaders})

@app.get("/login", summary="Login Form", tags=['WebPages'])
def login(request: Request):
    if not request.cookies.get('users_access_token'):
        return templates.TemplateResponse(name='login.html', context={"request": request})
    else:
        response = RedirectResponse(url='/')
        return response


@app.get("/", summary="Page of one operator", tags=['WebPages'])
def main(request: Request, reports=Depends(get_all_calls_by_oper), user = Depends(get_me)):
    filter_conditions = reports['req']
    filtered_reports = reports['res']
    stats = Statistic(list_of_records=filtered_reports, phone=user['phone_number']).get_user_stat()
    warning_flag = reports['warning']
    return templates.TemplateResponse(name="index.html",
                                      context={'request': request,
                                               'reports1': reports['res'],
                                               'user': user,
                                               'filter': filter_conditions,
                                               "stats": stats,
                                               'warning_flag': warning_flag,},

                                      )

@app.get("/teamleader", summary="Page of teamleader", tags=['WebPages'])
def main(request: Request, reports=Depends(get_group_oper_stat), user=Depends(get_me)):
    filter_conditions = reports['req']
    filtered_reports = reports['res']
    stats = Statistic(list_of_records=filtered_reports).get_group_stat()
    warning_flag = reports['warning']

    return templates.TemplateResponse(name="teamleader.html",
                                      context={'request': request,
                                               'reports2': reports['res'],
                                               'user': user,
                                               'filter': filter_conditions,
                                               "stats": stats,
                                               'warning_flag': warning_flag,
                                               },
                                      )

@app.get("/all", summary="Page of controller", tags=['WebPages'])
def main(request: Request, reports=Depends(get_group_oper_stat), user=Depends(get_me)):
    filter_conditions = reports['req']
    filtered_reports = reports['res']
    stats = Statistic(list_of_records=filtered_reports).get_group_stat()
    warning_flag = reports['warning']

    return templates.TemplateResponse(name="teamleader.html",
                                      context={'request': request,
                                               'reports2': reports['res'],
                                               'user': user,
                                               'filter': filter_conditions,
                                               "stats": stats,
                                               'warning_flag': warning_flag,
                                               },
                                      )

@app.get("/users", summary="Page of users list", tags=['WebPages'])
def get_users_list(request: Request, user=Depends(get_me), team_leaders=Depends(get_all_teamleader)):
    user_list = get_all_users()
    return templates.TemplateResponse(name="users.html",
                                      context={'request': request,
                                               'user': user,
                                               "group_leader_phones": team_leaders},
                                      )