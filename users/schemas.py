from typing import Optional, List

from pydantic import BaseModel, EmailStr, Field, validator
import re


class SUserRegister(BaseModel):
    password: str = Field(..., min_length=5, max_length=50, description="Пароль, от 5 до 50 знаков")
    phone_number: str = Field(..., description="Номер телефона")
    is_teamlead: bool = Field(False, description="Является руководителем группы")
    is_controller: bool = Field(False, description="Является контроллером")
    phone_teamleader: str = Field("", description="Телефон руководителя")

class SUserAuth(BaseModel):
    phone_number:str = Field(..., description="Номер телефона")
    password: str = Field(..., min_length=5, max_length=50, description="Пароль, от 5 до 50 знаков")

class SLeaderChange(BaseModel):
    phone_number:str = Field(..., description="Номер телефона")
    new_leader: str = Field("", description="Телефон руководителя")

class SNewRoles(BaseModel):
    phone_number: str = Field(..., description="Номер телефона")
    roles: List[str] = Field(..., description="Список новых ролей пользователя")

class SUserInfo():
    phone_number: str = Field(..., description="Номер телефона")
    role: str = Field(..., description="Роль")

class SUser(BaseModel):
    phone_number: str = Field(..., description="Номер телефона")
    is_operator: bool = Field(False, description="Является оператором")
    is_teamlead: bool = Field(False, description="Является руководителем группы")
    is_controller: bool = Field(False, description="Является контроллером")
    phone_teamleader: Optional[str] = Field("", description="Телефон руководителя")
