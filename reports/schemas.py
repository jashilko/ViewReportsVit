from datetime import datetime, date
from pydantic import BaseModel, Field, ConfigDict, field_validator


class SCRD(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    calldate: datetime = Field(..., description="Время звонка")
    src: str = Field(..., min_length=1, max_length=80, description="Кто звонил")
    dst: str = Field(..., min_length=1, max_length=80, description="Кому звонил")
    duration: int = Field(..., description="Длительность в секундах")
    billsec: int = Field(..., description="Что-то в секундах")
    disposition: str = Field(..., min_length=1, max_length=45, description="Статус")
    recordingfile: str = Field(..., max_length=255, description="Ссылка на файл с записью разговора")

    @field_validator("calldate")
    @classmethod
    def validate_calldate(cls, values: datetime) -> str:
        return values.strftime("%d-%m-%Y %H:%M:%S")