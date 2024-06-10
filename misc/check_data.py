from database.Query import Query

from sqlalchemy.orm import DeclarativeBase

from pydentic_schemes import schemes

from fastapi.exceptions import HTTPException

from typing import Type


async def check_data_in_db(
        model: Type[DeclarativeBase],
        schema: Type[schemes.BaseModel],
        error_message: str,
        **filter_data
) -> Type[schemes.BaseModel]:

    if await Query.get_data_by_filter(model=model, **filter_data):
        raise HTTPException(detail=error_message, status_code=500)

    return schema
