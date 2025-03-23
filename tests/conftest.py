import pytest
from httpx import AsyncClient
from main import app  # Подключаем FastAPI-приложение
from users.auth import get_password_hash
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