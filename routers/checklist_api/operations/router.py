from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from pydentic_schemes import schemes
from database.Query import Query
from database.models import Operation

from misc.check_data import check_data_in_db

router_operations = APIRouter(prefix='/operations')


async def verify_operation(operation: schemes.Operation):
    print(operation)
    if await Query.get_data_by_filter(model=Operation, verify=True, name_operation=operation.name_operation):
        raise HTTPException(detail='Операция уже существует', status_code=400)

    return operation


@router_operations.get('/getAll', tags=['operations'])
async def get_operations():

    operations = await Query.get_all_data(model=Operation)

    return operations


@router_operations.post('', tags=['operations'])
async def insert_operation(data=Depends(verify_operation)):
    if await Query.insert_data(model=Operation, name_operation=data.name_operation, hint=data.hint):
        return JSONResponse(content={"message": "Операция добавлена"}, status_code=201)

    return JSONResponse(content={"message": "Операция не создана"}, status_code=400)


@router_operations.get('/{operation_id}', tags=['operations'])
async def get_operation(operation_id: int):

    operation = await Query.get_data_by_id(model=Operation, model_id=operation_id)

    return operation


@router_operations.patch('/{operation_id}', tags=['operations'])
async def update_operation(operation_id: int, data_operation: schemes.Operation):

    if await Query.update_date(model=Operation, model_id=operation_id, **data_operation.dict()):
        return JSONResponse(content={"message": "Операция изменена"}, status_code=200)

    return JSONResponse(content={"message": "Произошла ошибка при изменении"}, status_code=500)


@router_operations.delete('/{operation_id}', tags=['operations'])
async def delete_operation(operation_id: int):

    if await Query.delete_data(model=Operation, model_id=operation_id):
        return JSONResponse(content={'message': 'Операция удалена'}, status_code=200)

    return JSONResponse(content={'message': 'Произошла ошибка при удалении'}, status_code=400)