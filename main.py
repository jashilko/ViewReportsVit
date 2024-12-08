from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import List, Optional
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from reports.router import router as router_cdr


app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory="public")
app.include_router(router_cdr)

# Модель для записи
class Recording(BaseModel):
    surname: str
    name: str
    file: str
    time: str

# Пример данных
recordings_data = [
    {"surname": "Иванов", "name": "Запись 1", "file": "audio/record1.mp3", "time": "09:30"},
    {"surname": "Петров", "name": "Запись 2", "file": "audio/record2.mp3", "time": "10:15"},
    {"surname": "Смирнов", "name": "Запись 3", "file": "audio/record3.mp3", "time": "11:45"},
    {"surname": "Иванов", "name": "Запись 4", "file": "audio/record4.mp3", "time": "14:00"},
    {"surname": "Смирнов", "name": "Запись 5", "file": "audio/record5.mp3", "time": "15:30"},
    {"surname": "Петров", "name": "Запись 6", "file": "audio/record6.mp3", "time": "17:00"},
]

# Модель для фильтров
class Filters(BaseModel):
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    surname: Optional[str] = None


@app.get("/login")
def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/")
def main(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/filter-recordings")
def filter_recordings(filters: Filters):
    # Применение фильтров
    filtered_recordings = [
        recording for recording in recordings_data
        if (filters.surname is None or filters.surname.lower() in recording['surname'].lower()) and
           (filters.start_time is None or recording['time'] >= filters.start_time) and
           (filters.end_time is None or recording['time'] <= filters.end_time)
    ]
    return filtered_recordings