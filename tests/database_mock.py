# tests/database_mock.py
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

# Инициализация тестовой SQLite базы
engine = create_async_engine("sqlite+aiosqlite:///:memory:")
session_maker = async_sessionmaker(engine, expire_on_commit=False)

# Для asterisk базы (если используется)
engine_asterisk = create_async_engine("sqlite+aiosqlite:///:memory:")
session_maker_asterisk = async_sessionmaker(engine_asterisk, expire_on_commit=False)

async def init_models():
    """Создание всех таблиц в тестовой базе"""
    from users.models import SiteUser  # Импортируем здесь, чтобы избежать циклических импортов
    async with engine.begin() as conn:
        await conn.run_sync(SiteUser.metadata.create_all)