
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.orm import DeclarativeBase, declared_attr
from config import get_db_url

DATABASE_URL = get_db_url()
engine = create_engine(DATABASE_URL)
session_maker = sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}"