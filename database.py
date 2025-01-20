
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.orm import DeclarativeBase, declared_attr, mapped_column
from config import get_db_url
from typing import Annotated

DATABASE_URL = get_db_url()
print('hello')
engine = create_engine("mysql+pymysql://user:Kostya!23@91.201.40.80:3306/db-vit")
session_maker = sessionmaker(engine, expire_on_commit=False)


# настройка аннотаций
int_pk = Annotated[int, mapped_column(primary_key=True)]
str_uniq = Annotated[str, mapped_column(unique=True, nullable=False)]
metadata_obj = MetaData()

class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}"

def create_table(cls):
    cls.__table__.create(engine, checkfirst=True)