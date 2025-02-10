import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    ADMIN_LOGIN: str
    START_PASS: str
    CONN_STR: str
    CONN_STR_ASTERISK: str
    AUDIO_PATH: str
    FILTER_MINUS_DAYS_FROM: int
    model_config = SettingsConfigDict(
        env_file='.env'
    )

settings = Settings()


def get_db_url():
    return settings.CONN_STR

def get_db_asterisk_url():
    return settings.CONN_STR_ASTERISK


def get_auth_data():
    return {"secret_key": settings.SECRET_KEY, "algorithm": settings.ALGORITHM}

def get_pass():
    return {"login": settings.ADMIN_LOGIN, "pass": settings.START_PASS}

def get_filter_minus_days_from() -> int:
    return settings.FILTER_MINUS_DAYS_FROM

