from fastapi import APIRouter, HTTPException, status, Depends, Request
from users.auth import get_password_hash, authenticate_user, create_access_token
from fastapi.responses import Response
from users.dao import UsersDAO, UsersManDAO
from users.schemas import SUserRegister, SUserAuth
from users.dependencies import get_current_user
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix='/auth', tags=['Auth'])

@router.post("/register/")
def register_user(user_data: SUserRegister) -> dict:
    user = UsersDAO.find_one_or_none(phone_number=user_data.phone_number)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Пользователь уже существует'
        )

    # Проверяем наличие телефона в БД
    phone_exists = UsersManDAO.find_one_or_none(username=user_data.phone_number)
    if not phone_exists:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail='Несуществующий телефон'
        )
    user_dict = user_data.dict()
    user_dict['password'] = get_password_hash(user_data.password)
    UsersDAO.add(**user_dict)
    return {'message': 'Вы успешно зарегистрированы!'}

@router.post("/login/")
def auth_user(response: Response, user_data: SUserAuth):
    check = authenticate_user(phone_number=user_data.phone_number, password=user_data.password)
    if check is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Неверный телефон или пароль')
    access_token = create_access_token({"sub": check.phone_number})
    response.set_cookie(key="users_access_token", value=access_token, httponly=True)
    return {'ok': True, 'access_token': access_token, 'refresh_token': None, 'message': 'Авторизация успешна!'}

@router.get("/me/")
def get_me(user_data: SUserAuth = Depends(get_current_user)):
    return user_data

@router.post("/logout/")
def logout_user(response: Response):
    response.delete_cookie(key="users_access_token")
    return {'ok': True, 'message': 'Пользователь успешно вышел из системы'}

@router.get("/all_operators", summary="Получить всех операторов")
def get_all_teamleader() -> list():
    return UsersDAO.all_teamleader()