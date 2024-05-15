from fastapi import APIRouter
from database.Query import Query
from database.models import User

service_router = APIRouter(
    prefix='/service',
    tags=['service_methods']
)


@service_router.get('/username')
async def get_username(username:str):

    if await Query.get_data_by_filter(model=User, username=username):
        return 'Пользователь существует'

    return 'Пользователь свободен'


@service_router.get('/email')
async def get_email(email:str):

    if await Query.get_data_by_filter(model=User, email=email):
        return 'Почта занята'

    return 'Почта свободна'
