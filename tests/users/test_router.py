from fastapi import Request, Depends

import pytest
from fastapi import status
from users.auth import get_password_hash, create_access_token
from users.dao import UsersDAO
from main import app
from fastapi.testclient import TestClient

from users.dependencies import get_current_user
from users.models import SiteUser
import asyncio

@pytest.fixture()
def mock_get_current_user_is_admin(monkeypatch, admin_user_class):
    async def mock_get_current_user():
        return admin_user_class
    app.dependency_overrides[get_current_user] = mock_get_current_user

@pytest.fixture()
def mock_get_current_user_is_usual(monkeypatch, usual_user_class):
    async def mock_get_current_user():
        return usual_user_class
    app.dependency_overrides[get_current_user] = mock_get_current_user

@pytest.fixture()
def mock_find_one_or_none_return_none(monkeypatch):
    async def mock_find_one_or_none(phone_number: str):
        return None
    monkeypatch.setattr(UsersDAO, "find_one_or_none", mock_find_one_or_none)

@pytest.fixture()
def mock_find_one_or_none_return_usual(monkeypatch, usual_user_class):
    async def mock_find_one_or_none(phone_number: str):
        return regular_user
    monkeypatch.setattr(UsersDAO, "find_one_or_none", mock_find_one_or_none)

@pytest.fixture()
def mock_add(monkeypatch):
    async def mock_add(**kwargs):
        return None
    monkeypatch.setattr(UsersDAO, "add", mock_add)

@pytest.fixture
def regular_user():
    """Фикстура обычного пользователя (без прав админа)."""
    return {"phone_number": "+987654321", "password": get_password_hash("userpass"), "is_admin": False}


@pytest.mark.asyncio
async def test_change_password_success(mock_get_current_user_is_admin, monkeypatch):
    client = TestClient(app)

    async def mock_update_password(phone_number, new_password):
        return None
    monkeypatch.setattr(UsersDAO, "update_password", mock_update_password)

    # Новый пароль
    new_password = "newsecurepassword"

    # Отправляем POST-запрос на /auth/change-password
    response = client.post(
        "/auth/change-password",
        json={"phone_number": "123123", "password": new_password}
    )
    # Проверяем статус-код и ответ
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"ok": True}


@pytest.mark.asyncio
async def test_register_user_success(mock_get_current_user_is_admin, mock_find_one_or_none_return_none,
                                     mock_add):
    client = TestClient(app)
    # Данные для регистрации
    user_data = {
        "phone_number": "+987654321",
        "password": "securepassword123",
        "is_teamlead": "false",
        "is_controller": "false",
        "phone_teamleader": "21ew"  # Пустая строка, так как это значение по умолчанию
    }
    response = client.post(
        "/auth/register",
        json=user_data
    )
    # Проверяем статус-код и ответ
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Вы успешно зарегистрированы!"}

@pytest.mark.asyncio
async def test_register_user_conflict(mock_get_current_user_is_admin, mock_find_one_or_none_return_usual):
    client = TestClient(app)
    # Данные для регистрации
    user_data = {
        "phone_number": "+987654321",
        "password": "securepassword123",
        "is_teamlead": "false",
        "is_controller": "false",
        "phone_teamleader": "21ew"  # Пустая строка, так как это значение по умолчанию
    }
    response = client.post(
        "/auth/register",
        json=user_data
    )

    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json() == {"detail": "Пользователь уже существует"}


@pytest.mark.asyncio
async def test_register_user_not_admin(mock_get_current_user_is_usual, mock_find_one_or_none_return_none):
    client = TestClient(app)
    # Данные для регистрации
    user_data = {
        "phone_number": "+987654321",
        "password": "securepassword123",
        "is_teamlead": "false",
        "is_controller": "false",
        "phone_teamleader": "21ew"  # Пустая строка, так как это значение по умолчанию
    }
    response = client.post(
        "/auth/register",
        json=user_data
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == {"detail": "Недостаточно прав"}

@pytest.mark.asyncio
async def test_login_success(monkeypatch, usual_user_class, mock_find_one_or_none_return_usual):
    client = TestClient(app)

    # Мокируем authenticate_user, чтобы он возвращал usual_user_class
    async def mock_authenticate_user(phone_number: str, password: str):
        return usual_user_class
    monkeypatch.setattr("users.auth.authenticate_user", mock_authenticate_user)

    # Мокируем create_access_token, чтобы он возвращал фиктивный токен
    def mock_create_access_token(data: dict):
        return "fake_access_token"
    monkeypatch.setattr("users.auth.create_access_token", mock_create_access_token)

    # Данные для аутентификации
    user_data = {
        "phone_number": "123213",
        "password": "pass111"
    }

    # Отправляем POST-запрос на /auth/login/
    response = client.post(
        "/auth/login/",
        json=user_data,
    )

    # Проверяем статус-код и ответ
    print("Response Body:", response.json())  # Для отладки
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        'ok': True,
        'access_token': "fake_access_token",  # Используем фиктивный токен
        'refresh_token': None,
        'message': 'Авторизация успешна!'
    }
