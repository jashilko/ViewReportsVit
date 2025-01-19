import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    SECRET_KEY: str
    ALGORITHM: str
    ADMIN_LOGIN: str
    START_PASS: str
    CONN_STR: str
    IS_PROM: str
    model_config = SettingsConfigDict(
        env_file='.env'
    )

settings = Settings()


def get_db_url():
    if settings.IS_PROM == 'Y':
        return settings.CONN_STR
    else:
        return (f"mysql+pymysql://{settings.DB_USER}:{settings.DB_PASSWORD}@"
                f"{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}")


def get_auth_data():
    return {"secret_key": settings.SECRET_KEY, "algorithm": settings.ALGORITHM}

def get_pass():
    return {"login": settings.ADMIN_LOGIN, "pass": settings.START_PASS}