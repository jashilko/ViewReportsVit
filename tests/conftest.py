import pytest
from httpx import AsyncClient
from main import app  # Подключаем FastAPI-приложение
from users.auth import get_password_hash
from users.dao import UsersDAO
from users.models import SiteUser
import pytest_asyncio
from tests import database_mock
from sqlalchemy import insert
from users.models import SiteUser

@pytest.fixture
async def async_client():
    """Фикстура для тестирования FastAPI."""
    print("Создание тестового клиента...")  # ➜ Добавим отладочный вывод
    async with AsyncClient(app=app, base_url="http://test") as client:
        print("Тестовый клиент создан!")  # ➜ Отладка: Убедимся, что клиент реально создаётся
        yield client

@pytest.fixture
def admin_user():
    """Фикстура тестового админа."""
    return {
        "phone_number": "+123456789",
        "password": get_password_hash("adminpass"),
        "is_admin": True,
        "token": "fake_admin_token"  # Добавляем токен
    }

@pytest.fixture
def admin_user_class():
    return SiteUser(
        id=1,
        phone_number="+123456789",
        password=get_password_hash("adminpass"),
        is_admin=True,
        is_operator=False,
        is_teamlead=False,
        is_controller=False,
        phone_teamleader=""
    )
@pytest.fixture
def usual_user_class():
    return SiteUser(
        id=2,
        phone_number="+987654321",
        password=get_password_hash("userpass"),
        is_admin=False,
        is_operator=True,
        is_teamlead=False,
        is_controller=False,
        phone_teamleader="3242423"
    )

@pytest.fixture
def mock_user():
    password = "securepassword"
    hashed_password = get_password_hash(password)
    return type("User", (), {"phone_number": "+123456789", "password": hashed_password})

@pytest.fixture(autouse=True)
def mock_database(monkeypatch):
    # Подменяем импорты во всех местах
    monkeypatch.setattr('database.session_maker', database_mock.session_maker)
    monkeypatch.setattr('users.dao.session_maker', database_mock.session_maker)
    monkeypatch.setattr('base.session_maker', database_mock.session_maker)



@pytest_asyncio.fixture(scope="function")
async def setup_test_db():
    from tests.database_mock import engine, init_models
    await init_models()
    yield
    await engine.dispose()


@pytest_asyncio.fixture
async def test_session():
    from tests.database_mock import session_maker
    async with session_maker() as session:
        yield session


@pytest_asyncio.fixture
async def add_test_users(test_session):
    test_data = [
        {"id": 1, "phone_number": "999", "password": "123", "is_operator": True,
         "is_teamlead": True, "is_controller": True, "is_admin": True, "phone_teamleader": "101"},
        {"id": 2, "phone_number": "101", "password": "123", "is_operator": True,
         "is_teamlead": True, "is_controller": False, "is_admin": False, "phone_teamleader": "101"},
        {"id": 3, "phone_number": "102", "password": "123", "is_operator": True,
         "is_teamlead": False, "is_controller": False, "is_admin": False, "phone_teamleader": "101"},
    ]
    await test_session.execute(insert(SiteUser), test_data)
    await test_session.commit()

@pytest.fixture()
def mock_find_one_or_none_return_none(monkeypatch):
    async def mock_find_one_or_none(phone_number: str):
        return None
    monkeypatch.setattr(UsersDAO, "find_one_or_none", mock_find_one_or_none)

@pytest.fixture
def regular_user():
    """Фикстура обычного пользователя (без прав админа)."""
    return {"phone_number": "+987654321", "password": get_password_hash("userpass"), "is_admin": False}

@pytest.fixture()
def mock_find_one_or_none_return_usual(monkeypatch, usual_user_class):
    async def mock_find_one_or_none(phone_number: str):
        return regular_user
    monkeypatch.setattr(UsersDAO, "find_one_or_none", mock_find_one_or_none)