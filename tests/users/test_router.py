from unittest.mock import AsyncMock

from fastapi import Request, Depends

import pytest
from fastapi import status
from users.auth import get_password_hash, create_access_token
from users.dao import UsersDAO, UsersNameDAO
from main import app
from fastapi.testclient import TestClient
import users

from users.dependencies import get_current_user
from users.auth import authenticate_user
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
def mock_add(monkeypatch):
    async def mock_add(**kwargs):
        return None
    monkeypatch.setattr(UsersDAO, "add", mock_add)

@pytest.fixture
def mock_get_operators_name(monkeypatch):
    async def mock_operators_name():
        return {
            "+123456789": "Иван Иванов",
            "+987654321": "Петр Петров",
            "+333": "Вася Пупкин",

        }
    # Подменяем функцию get_operators_name на мок
    # monkeypatch.setattr("users.router.get_operators_name", mock_operators_name)
    monkeypatch.setattr(UsersNameDAO, "all_operator_list", mock_operators_name)

@pytest.fixture()
def mock_find_all(monkeypatch, usual_user_class, admin_user_class):
    async def mock_all(is_teamlead=True):
        return [usual_user_class, admin_user_class]
    monkeypatch.setattr(UsersDAO, "find_all", mock_all)

@pytest.fixture()
def mock_userdao_update(monkeypatch, usual_user_class, admin_user_class):
    async def mock_update(phone_number: str, **updates):
        return None
    monkeypatch.setattr(UsersDAO, "update_by_phone", mock_update)

@pytest.mark.asyncio
async def test_change_password_success(mock_get_current_user_is_admin, mock_userdao_update):
    client = TestClient(app)

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
@pytest.mark.skip(reason='Пока не работает')
async def test_login_success(monkeypatch, usual_user_class, mock_find_one_or_none_return_usual):
    client = TestClient(app)


    # Мокируем create_access_token, чтобы он возвращал фиктивный токен
    def mock_create_access_token(data: dict):
        print("Mocked create_access_token called with:", data)
        return "fake_access_token"
    monkeypatch.setattr("users.auth.create_access_token", mock_create_access_token)

    # Данные для аутентификации
    user_data = {
        "phone_number": "+123456789",  # Номер телефона должен совпадать с usual_user_class
        "password": "userpass"  # Пароль должен совпадать с usual_user_class
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

@pytest.mark.asyncio
async def test_logout_sucsess():
    client = TestClient(app)
    responce = client.post(
        "/auth/logout"
    )

    print(responce.cookies)
    assert responce.json() == {
        'ok': True,
        'message': 'Пользователь успешно вышел из системы'
    }

@pytest.mark.asyncio
async def test_get_all_teamleader(mock_find_all, mock_get_operators_name):
    client = TestClient(app)
    response = client.get("/auth/all_teamleaders")

    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    data = response.json()
    assert "+123456789" in data
    assert "+987654321" in data
    assert data["+123456789"] == "Иван Иванов"

@pytest.mark.asyncio
async def test_get_all_users(mock_find_all, mock_get_operators_name):
    client = TestClient(app)
    response = client.get("/auth/all_users")
    assert response.status_code == 200
    # Внутри список
    assert isinstance(response.json(), list)
    data = response.json()
    # Первый элемент списка - словарь
    assert isinstance(data[0], dict)

@pytest.mark.asyncio
async def test_change_password_not_admin(mock_get_current_user_is_usual):
    client = TestClient(app)
    user_data = {
        "phone_number": "+123456789",  # Номер телефона должен совпадать с usual_user_class
        "password": "userpass"  # Пароль должен совпадать с usual_user_class
    }
    response = client.post(
        "/auth/change-password",
        json=user_data
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_change_leader_not_admin(mock_get_current_user_is_usual):
    client = TestClient(app)
    user_data = {
        "phone_number": "+123456789",
        "new_leader": "+8995555"
    }
    response = client.post(
        "/auth/change-leader",
        json=user_data
    )
    assert response.status_code == 403

@pytest.mark.asyncio
async def test_change_leader(mock_get_current_user_is_admin, mock_userdao_update):

    client = TestClient(app)
    user_data = {
        "phone_number": "+123456789",
        "new_leader": "+8995555"
    }
    response = client.post(
        "/auth/change-leader",
        json=user_data
    )
    assert response.status_code == 200
    assert response.json() == {'ok': True}

@pytest.mark.asyncio
async def test_change_roles_not_admin(mock_get_current_user_is_usual):
    client = TestClient(app)
    user_data = {
        "phone_number": "+123456789",
        "roles": ["213", "wqe"]
    }
    response = client.post(
        "/auth/change-roles",
        json=user_data
    )
    assert response.status_code == 403

@pytest.mark.asyncio
async def test_change_roles(mock_get_current_user_is_admin, mock_userdao_update):
    client = TestClient(app)
    user_data = {
        "phone_number": "+123456789",
        "roles": ["ddqwd", "wqw"]
    }
    response = client.post(
        "/auth/change-roles",
        json=user_data
    )
    assert response.status_code == 200
    assert response.json() == {'ok': True}

@pytest.mark.asyncio
async def test_change_roles_error_role_type(mock_get_current_user_is_admin, mock_userdao_update):
    client = TestClient(app)
    user_data = {
        "phone_number": "+123456789",
        "roles": "eqweq"
    }
    response = client.post(
        "/auth/change-roles",
        json=user_data
    )
    assert response.status_code == 422