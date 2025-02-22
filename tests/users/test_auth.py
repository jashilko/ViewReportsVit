import pytest
from users.auth import get_password_hash, verify_password, create_access_token, authenticate_user
from passlib.context import CryptContext
from passlib.exc import UnknownHashError
from config import get_auth_data
from jose import jwt
from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock

from users.dao import UsersDAO

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def test_get_password_hash():
    password = "securepassword"
    hashed_password = get_password_hash(password)

    assert isinstance(hashed_password, str), "Хэш должен быть строкой"
    assert hashed_password != password, "Хэш не должен совпадать с паролем"
    assert pwd_context.verify(password, hashed_password), "Хэш не соответствует паролю"

    another_password = "differentpassword"
    another_hashed_password = get_password_hash(another_password)
    assert hashed_password != another_hashed_password, "Разные пароли должны давать разные хэши"

@pytest.fixture(scope='module')
def hashed_password():
    password = "securepassword"
    return password, get_password_hash(password)

def test_verify_password_correct(hashed_password):
    password, hashed = hashed_password
    assert verify_password(password, hashed) is True, "Пароль должен быть валиден"

def test_verify_password_incorrect(hashed_password):
    _, hashed = hashed_password
    assert verify_password("wrongpassword", hashed) is False, "Пароль не должен совпадать"

@pytest.mark.parametrize("password", ["", "  "])
def test_verify_password_empty(password, hashed_password):
    _, hashed = hashed_password
    assert verify_password(password, hashed) is False, "Пустой пароль не должен совпадать с хэшем"

def test_verify_password_long():
    long_password = "a" * 1000
    hashed = get_password_hash(long_password)
    assert verify_password(long_password, hashed) is True, "Длинный пароль должен верифицироваться"


def test_verify_password_with_empty_hash():
    with pytest.raises(UnknownHashError):
        verify_password("somepassword", "")

@pytest.mark.xfail(reason='Намеренный провал', raises=ValueError)
def test_verify_password_with_random_hash():
    assert verify_password("somepassword", "$2b$12$somefakestringthatdoesnotmatch") is False, "Неверный хэш не должен проходить проверку"

def test_verify_password():
    assert verify_password('123456', '$2b$12$CphH1eIeV/YpilZZVCEwiec1SYBqTG3o4IozVL.D4nUNZYfyVlSq6')

def test_verify_password_with_random_hash1():
    with pytest.raises(ValueError):
        verify_password("somepassword", "$2b$12$somefakestringthatdoesnotmatch")


@pytest.fixture
def test_data():
    return {"sub": "101", }

# Токен - строка
def test_create_access_token(test_data):
    token = create_access_token(test_data)
    assert isinstance(token, str), "Токен должен быть строкой"
    assert len(token) > 0, "Токен не должен быть пустым"


def test_decode_access_token(test_data):
    token = create_access_token(test_data)
    auth_data = get_auth_data()
    decoded = jwt.decode(token, auth_data['secret_key'], algorithms=[auth_data['algorithm']])
    assert decoded["sub"] == test_data["sub"], "Декодированный sub должен совпадать"


def test_access_token_expiration(test_data):
    token = create_access_token(test_data)
    auth_data = get_auth_data()
    decoded = jwt.decode(token, auth_data['secret_key'], algorithms=[auth_data['algorithm']])
    exp = datetime.fromtimestamp(decoded["exp"], tz=timezone.utc)
    expected_exp = datetime.now(timezone.utc) + timedelta(days=30)
    assert abs((exp - expected_exp).total_seconds()) < 5, "Срок действия токена должен быть 30 дней"


@pytest.mark.parametrize("data", [
    {"user_id": 1},
    {"user_id": 42, "role": "editor"},
    {"username": "test_user", "permissions": ["read", "write"]}
])
def test_access_token_various_data(data):
    token = create_access_token(data)
    auth_data = get_auth_data()

    decoded = jwt.decode(token, auth_data['secret_key'], algorithms=[auth_data['algorithm']])

    for key in data:
        assert decoded[key] == data[key], f"Поле {key} должно совпадать"

@pytest.fixture
def mock_user():
    password = "securepassword"
    hashed_password = get_password_hash(password)
    return type("User", (), {"phone_number": "+123456789", "password": hashed_password})

@pytest.mark.asyncio
async def test_authenticate_user_success(monkeypatch, mock_user):
    async_mock = AsyncMock(return_value=mock_user)
    monkeypatch.setattr(UsersDAO, "find_one_or_none", async_mock)

    user = await authenticate_user("+123456789", "securepassword")
    assert user is not None, "Должен вернуться пользователь"
    assert user.phone_number == "+123456789", "Телефон пользователя должен совпадать"

@pytest.mark.asyncio
async def test_authenticate_user_failed(monkeypatch, mock_user):
    async_mock = AsyncMock(return_value=mock_user)
    monkeypatch.setattr(UsersDAO, "find_one_or_none", async_mock)

    user = await authenticate_user("+123456789", "securepa")
    assert user is None, "Должно вернуться None при неверном пароле"
