from fastapi import FastAPI, Request, Depends
from pydantic import BaseModel
from typing import List, Optional
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from reports.router import router as router_cdr
from users.router import router as router_users
from reports.router import get_all_cdr


app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory="public")
app.include_router(router_cdr)
app.include_router(router_users)


@app.get("/login")
def login(request: Request):
    return templates.TemplateResponse(name='login.html', context={"request": request})


@app.get("/")
def main(request: Request, reports=Depends(get_all_cdr)):
    return templates.TemplateResponse(name="index.html", context={'request': request, 'reports1': reports})
