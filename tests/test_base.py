# tests/test_base.py
import pytest
from users.dao import UsersDAO


@pytest.mark.asyncio
async def test_find_all(setup_test_db, add_test_users):

    result = await UsersDAO.find_all()
    phone_numbers = {item.phone_number for item in result}
    print(f"Found phone numbers: {phone_numbers}")

    assert len(result) == 3
    assert phone_numbers == {"999", "101", "102"}


@pytest.mark.asyncio
async def test_find_all_with_filter(setup_test_db, add_test_users):
    # Тест с фильтром
    result = await UsersDAO.find_all(phone_number="101")

    assert len(result) == 1
    assert result[0].id == 2


@pytest.mark.asyncio
async def test_find_one_or_none(setup_test_db, add_test_users):
    """Тестирование find_one_or_none с различными сценариями"""

    # 1. Проверка нахождения существующего пользователя
    user = await UsersDAO.find_one_or_none(phone_number="101")
    assert user is not None
    assert user.id == 2
    assert user.phone_number == "101"

    # 2. Проверка нахождения несуществующего пользователя
    non_existent_user = await UsersDAO.find_one_or_none(phone_number="000")
    assert non_existent_user is None

    # 3. Проверка с составным фильтром
    admin_user = await UsersDAO.find_one_or_none(phone_number="999", is_admin=True)
    assert admin_user is not None
    assert admin_user.id == 1

    # 4. Проверка с составным фильтром, где нет совпадений
    non_matching_user = await UsersDAO.find_one_or_none(phone_number="101", is_admin=True)
    assert non_matching_user is None


@pytest.mark.asyncio
async def test_add_success(setup_test_db):
    """Тест успешного добавления записи"""
    # 1. Подготовка тестовых данных
    user_data = {
        "id": 7,
        "phone_number": "777",
        "password": "123",
        "is_operator": True,
        "is_teamlead": False,
        "is_controller": False,
        "is_admin": False,
        "phone_teamleader": "101"
    }

    # 2. Вызов тестируемого метода
    new_user = await UsersDAO.add(**user_data)

    # 3. Проверки
    assert new_user is not None
    assert new_user.id == 7

    # Проверяем, что запись действительно сохранена в БД
    db_user = await UsersDAO.find_one_or_none(id=7)
    assert db_user is not None
    assert db_user.phone_number == "777"
    assert db_user.is_operator is True

@pytest.mark.asyncio
async def test_add_with_invalid_data(setup_test_db):
    """Тест добавления с некорректными данными"""
    # Пытаемся добавить пользователя без обязательного поля phone_number
    with pytest.raises(Exception):
        await UsersDAO.add(
            id=8,
            password="123",
            is_operator=True
        )

@pytest.mark.asyncio
async def test_add_duplicate(setup_test_db, add_test_users):
    """Тест добавления дубликата (уникальное поле phone_number)"""
    # Пытаемся добавить пользователя с существующим phone_number
    with pytest.raises(Exception):
        await UsersDAO.add(
            id=9,
            phone_number="101",  # Уже существует
            password="123",
            is_operator=True
        )

@pytest.mark.asyncio
async def test_update_success(setup_test_db, add_test_users):
    # 1. Получаем исходные данные пользователя
    original_user = await UsersDAO.find_one_or_none(id=2)
    assert original_user is not None
    original_phone = original_user.phone_number

    # 2. Выполняем обновление (меняем номер телефона)
    updated_user = await UsersDAO.update(2, phone_number="888")

    # 3. Проверяем возвращаемое значение
    assert updated_user is not None
    assert updated_user.id == 2
    assert updated_user.phone_number == "888"

    # 4. Проверяем, что изменения сохранились в БД
    db_user = await UsersDAO.find_one_or_none(id=2)
    assert db_user is not None
    assert db_user.phone_number == "888"

    # 5. Проверяем, что другие поля не изменились
    assert db_user.is_operator == original_user.is_operator
    assert db_user.is_teamlead == original_user.is_teamlead