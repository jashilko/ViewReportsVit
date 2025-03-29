import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import insert, select
from users.models import SiteUser  # Импорт модели
from users.dao import UsersDAO


@pytest.mark.asyncio
async def test_users_dao_update_by_phone_none(setup_test_db, mock_find_one_or_none_return_none):
    test_phone = "+79998887766"
    test_updates = {"name": "New Name"}
    # Проверяем что вызовется исключение
    with pytest.raises(ValueError) as exc_info:
        await UsersDAO.update_by_phone(test_phone, **test_updates)

    assert str(exc_info.value) == f"Пользователь с номером {test_phone} не найден"


