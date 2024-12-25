from fastapi import FastAPI, Request, Depends, Form
from pydantic import BaseModel
from typing import List, Optional
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
import datetime

from reports.model import CDR
from reports.rb import RBCdr
from reports.router import router as router_cdr
from users.router import router as router_users
from reports.router import get_all_cdr, get_all_calls_by_oper
from users.router import get_me
from pages.router import router as router_pages
from reports.dao import CdrDAO


app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory="public")
app.include_router(router_cdr)
app.include_router(router_users)
app.include_router(router_pages)


@app.get("/registr")
def login(request: Request):
    return templates.TemplateResponse(name='registr.html', context={"request": request})

@app.get("/login")
def login(request: Request):
    if not request.cookies.get('users_access_token'):
        return templates.TemplateResponse(name='login.html', context={"request": request})
    else:
        response = RedirectResponse(url='/')
        return response


@app.get("/")
def main(request: Request, reports=Depends(get_all_calls_by_oper), user = Depends(get_me)):
    filter_conditions = reports['req']
    filtered_reports = reports['res']
    total_calls = len(filtered_reports)
    incoming_calls = len([r for r in filtered_reports if r["dst"] == user.phone_number])
    outgoing_calls = total_calls - incoming_calls
    total_billsec = sum(r["billsec"] for r in filtered_reports)
    average_call_duration = total_billsec / total_calls if total_calls > 0 else 0
    stats = {
        "total_calls": total_calls,
        "incoming_calls": incoming_calls,
        "outgoing_calls": outgoing_calls,
        "total_billsec": total_billsec,
        "average_call_duration": average_call_duration,
    }
    warning_flag = reports['warning']

    return templates.TemplateResponse(name="index.html",
                                      context={'request': request,
                                               'reports1': reports['res'],
                                               'user': user,
                                               'filter': filter_conditions,
                                               "stats": stats,
                                               'warning_flag': warning_flag,},

                                      )
