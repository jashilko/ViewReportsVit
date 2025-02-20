from sqlalchemy.orm import DeclarativeBase, declared_attr, mapped_column
from config import get_db_url, get_db_asterisk_url
from typing import Annotated
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs

DATABASE_URL = get_db_url()
DATABASE_URL_ASTERISK = get_db_asterisk_url()
try:
    engine = create_async_engine(DATABASE_URL)
    connection = engine.connect()
    print("Connection successful!")
except OperationalError as e:
    print(f"OperationalError: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
session_maker = async_sessionmaker(engine, expire_on_commit=False)

try:
    engine_asterisk = create_async_engine(DATABASE_URL_ASTERISK)
    connection_asterisk = engine_asterisk.connect()
    print("Connection asterisk successful!")
except OperationalError as e:
    print(f"OperationalError: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
session_maker_asterisk = async_sessionmaker(engine_asterisk, expire_on_commit=False)

# настройка аннотаций
int_pk = Annotated[int, mapped_column(primary_key=True)]
str_uniq = Annotated[str, mapped_column(unique=True, nullable=False)]

class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}"

async def create_table(cls):
    async with engine.begin() as conn:
        await conn.run_sync(cls.__table__.create, checkfirst=True)