import pytest

from config import get_auth_data
from tests.conftest import regular_user
from users.auth import create_access_token
from users.dependencies import get_token, get_current_user

from fastapi import HTTPException
from fastapi import status
from datetime import datetime, timedelta, timezone
from jose import jwt
from fastapi import FastAPI

@pytest.fixture
def mock_request_with_token():
    class MockRequest:
        def __init__(self, token_value):
            self.cookies = {'users_access_token': token_value}

    return MockRequest("test_token_123")

@pytest.fixture
def mock_request_without_token():
    class MockRequest:
        def __init__(self):
            self.cookies = {}

    return MockRequest()


def test_dependencies_get_token_with_token(mock_request_with_token):
    # Проверяем, что функция возвращает токен, когда он есть в cookies
    token = get_token(mock_request_with_token)
    assert token == "test_token_123"


def test_dependencies_get_token_without_token(mock_request_without_token):
    # Проверяем, что функция вызывает исключение, когда токена нет в cookies
    with pytest.raises(HTTPException) as exc_info:
        get_token(mock_request_without_token)

    # Проверяем статус код и заголовки в исключении
    assert exc_info.value.status_code == status.HTTP_307_TEMPORARY_REDIRECT
    assert exc_info.value.headers == {'Location': '/login'}


@pytest.mark.asyncio
async def test_dependencies_get_current_user_valid(mock_find_one_or_none_return_usual):
        token = create_access_token({"sub": "+987654321"})
        user = await get_current_user(token=token)
        assert user["phone_number"] == regular_user()["phone_number"]


@pytest.mark.asyncio
async def test_dependencies_get_current_user_invalid_token():
    with pytest.raises(HTTPException) as exc_info:
        await get_current_user(token="invalid_token")

    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc_info.value.detail == 'Токен не валидный!'


@pytest.mark.asyncio
async def test_dependencies_get_current_user_expired_token():
    data = {"sub": "+987654321"}
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=-1)
    to_encode.update({"exp": expire})
    auth_data = get_auth_data()
    encode_jwt = jwt.encode(to_encode, auth_data['secret_key'], algorithm=auth_data['algorithm'])
    with pytest.raises(HTTPException) as exc_info:
        await get_current_user(token=encode_jwt)

    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc_info.value.detail == 'Токен истек'


@pytest.mark.asyncio
async def test_dependencies_get_current_user_no_sub_in_token():
    expire = datetime.now(timezone.utc) + timedelta(days=30)
    to_encode = {"exp": expire}
    auth_data = get_auth_data()
    encode_jwt = jwt.encode(to_encode, auth_data['secret_key'], algorithm=auth_data['algorithm'])
    with pytest.raises(HTTPException) as exc_info:
        await get_current_user(token=encode_jwt)

    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc_info.value.detail == 'Не найден ID пользователя'

@pytest.mark.asyncio
async def test_dependencies_get_current_user_not_found(mock_find_one_or_none_return_none):
    token = create_access_token({"sub": "+987654321"})
    with pytest.raises(HTTPException) as exc_info:
        await  get_current_user(token=token)

    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc_info.value.detail == 'User not found'