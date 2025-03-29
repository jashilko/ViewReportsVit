from fastapi import APIRouter, HTTPException, status, Depends
from users.auth import get_password_hash, authenticate_user, create_access_token
from fastapi.responses import Response
from users.dao import UsersDAO, UsersNameDAO
from users.schemas import SUserRegister, SUserAuth, SLeaderChange, SNewRoles
from users.dependencies import get_current_user

router = APIRouter(prefix='/auth', tags=['Auth'])


async def register_admin(cred):
    if not await UsersDAO.find_one_or_none(**{'is_admin': True}):
        user_dict = {}
        user_dict['phone_number'] = cred['login']
        user_dict['password'] = get_password_hash(cred['pass'])
        user_dict['is_admin'] = True
        user_dict['phone_teamleader'] = '100'
        await UsersDAO.add(**user_dict)
        print('Админ создан')
    else:
        print('Админ уже существует')


@router.post("/register/")
async def register_user(user_data: SUserRegister, user=Depends(get_current_user)) -> dict:
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Недостаточно прав'
        )
    user = await UsersDAO.find_one_or_none(phone_number=user_data.phone_number)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Пользователь уже существует'
        )

    user_dict = user_data.dict()
    user_dict['password'] = get_password_hash(user_data.password)
    await UsersDAO.add(**user_dict)
    return {'message': 'Вы успешно зарегистрированы!'}


@router.post("/login/")
async def auth_user(response: Response, user_data: SUserAuth):
    check = await authenticate_user(phone_number=user_data.phone_number, password=user_data.password)
    if check is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Неверный телефон или пароль')
    access_token = create_access_token({"sub": check.phone_number})
    response.set_cookie(key="users_access_token", value=access_token, httponly=True)
    return {'ok': True, 'access_token': access_token, 'refresh_token': None, 'message': 'Авторизация успешна!'}


@router.get("/me/")
async def get_me(user_data=Depends(get_current_user)):
    return user_data.to_dict()


@router.post("/logout/")
async def logout_user(response: Response):
    response.delete_cookie(key="users_access_token")
    return {'ok': True, 'message': 'Пользователь успешно вышел из системы'}


@router.get("/all_teamleaders", summary="Get all teamleaders")
async def get_all_teamleader() -> dict():
    all_team_leaders = await UsersDAO.find_all(is_teamlead=True)
    operator_names = await get_operators_name()
    # Преобразуйте данные  в словари
    user_dict = {}
    for user in all_team_leaders:
        user_dict[user.phone_number] = operator_names.get(user.phone_number, "БезИмени")
    return user_dict


@router.get("/all_users", summary="Get all users")
async def get_all_users():
    operator_names = await get_operators_name()  # Получаем список операторов
    userlist = await UsersDAO.find_all()  # Получаем список пользователей
    # Преобразуйте данные  в словари
    user_data = []
    for user in userlist:
        user_dict = user.to_dict()
        user_dict["oper_name"] = operator_names.get(user_dict["phone_number"], "БезИмени")
        user_data.append(user_dict)

    return user_data


@router.post("/change-password", summary="Set new password")
async def post_change_password(new_pass: SUserAuth, user=Depends(get_current_user)):
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Недостаточно прав'
        )
    hash_new_pass = get_password_hash(new_pass.password)
    await UsersDAO.update_by_phone(new_pass.phone_number, password=hash_new_pass)
    return {'ok': True}


@router.post("/change-leader", summary="Set new leader")
async def post_change_leader(new_lead: SLeaderChange, user=Depends(get_current_user)):
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Недостаточно прав'
        )
    await UsersDAO.update_by_phone(new_lead.phone_number, phone_teamleader=new_lead.new_leader)
    return {'ok': True}


@router.post("/change-roles", summary="Set new roles")
async def post_change_leader(new_roles: SNewRoles, user=Depends(get_current_user)):
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Недостаточно прав'
        )
    await UsersDAO.update_by_phone(new_roles.phone_number,
                                   is_operator=True if "Оператор" in new_roles.roles else False,
                                   is_teamlead=True if "Руководитель" in new_roles.roles else False,
                                   is_controller=True if "Контроллер" in new_roles.roles else False)
    return {'ok': True}


@router.get("/all_operators_name", summary="Get operators with names")
async def get_operators_name():
    return await UsersNameDAO.all_operator_list()
