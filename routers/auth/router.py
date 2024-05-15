from fastapi import APIRouter, Depends, HTTPException, Form
from fastapi.security import OAuth2PasswordBearer

from pydentic_schemes.schemes import UserRegister, UserLogin

from database.Query import Query
from database import models

from .auth import *

router_auth = APIRouter(
    prefix='/auth',
    tags=['Auth']
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/auth/login')


async def validate_user_login(user_data: UserLogin):
    #login: str = Form(), password: str = Form()

    user = await Query.get_data_by_filter(model=models.User, username=user_data.login)

    if not user:
        raise HTTPException(status_code=400, detail='Неправильно введено имя')

    if not validate_password(password=user_data.password, hashed_password=user[0]['hashed_password']):
        raise HTTPException(status_code=400, detail='Неправильно введен пароль')

    return user


async def get_current_user(token: str = Depends(oauth2_scheme)):

    decoded_data = verify_jwt_token(token=token, algorithm='HS256')

    if not decoded_data:
        raise HTTPException(status_code=400, detail=f'Невалидный токен {token}')

    user = await Query.get_data_by_filter(model=models.User, username=decoded_data['Username'])

    if not user:
        raise HTTPException(status_code=400, detail='Пользователь не найден')

    return user


async def verify_user_data(user_data: UserRegister):

    if await Query.get_data_by_filter(model=models.User,  verify=True, username=user_data.username, email=user_data.email):
        raise HTTPException(status_code=400, detail='Данный пользователь занят')

    return user_data


@router_auth.post('/register')
async def register_user(user_data: UserRegister = Depends(verify_user_data)):

    if await Query.insert_data(model=models.User, username=user_data.username, email=user_data.email, hashed_password=hash_password(user_data.password), is_superuser=False):
        return HTTPException(status_code=201, detail='Пользователь создан')

    raise HTTPException(status_code=400, detail='Произошла ошибка при создании пользователя')


@router_auth.post('/login')
def login_user(user=Depends(validate_user_login)):

    jwt_payload = {
        'User_id': user[0]['id'],
        "Username": user[0]['username'],
        "Email": user[0]['email']
    }

    jwt_token = create_jwt_token(payload=jwt_payload, algorithm='HS256')

    return {'access_token': jwt_token,
            'token_type': "Bearer"}


@router_auth.get('/test')
def auth_test(user=Depends(get_current_user)):

    return f'Привет {user["username"]}'
