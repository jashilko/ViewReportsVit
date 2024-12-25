from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta, timezone
from config import get_auth_data
from users.dao import UsersDAO


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict) -> str:
    print(data)
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=30)
    to_encode.update({"exp": expire})
    auth_data = get_auth_data()
    encode_jwt = jwt.encode(to_encode, auth_data['secret_key'], algorithm=auth_data['algorithm'])
    return encode_jwt

def authenticate_user(phone_number: str, password: str):
    user = UsersDAO.find_one_or_none(phone_number=phone_number)
    if not user or verify_password(plain_password=password, hashed_password=user.password) is False:
        return None
    return user