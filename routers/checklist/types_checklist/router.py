from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from pydentic_schemes import schemes
from database.Query import Query
from database.models import Operation, TypeCheckList, TypeCheckListOperations

router_type_checklist = APIRouter(prefix='/type_checklist', tags=['Type_checklist'])


async def verify_type_operation(data: schemes.TypeCheckListOperations):

    if not await Query.get_data_by_id(model=TypeCheckList, model_id=data.type_id, verify=True):
        raise HTTPException(detail='Данный тип не заведен', status_code=400)

    if not await Query.get_data_by_id(model=Operation, model_id=data.operation_id, verify=True):
        raise HTTPException(detail='Данная операция не заведена', status_code=400)

    return data


async def verify_type_checklist(type_checklist: schemes.TypeCheckList):

    if await Query.get_data_by_filter(model=TypeCheckList, verify=True, type_name=type_checklist.type_name):
        raise HTTPException(detail='Тип уже существует', status_code=400)

    return type_checklist


async def verify_update_type_checklist(type_checklist: schemes.TypeCheckList, type_id: int):

    if await Query.get_data_by_filter(model=TypeCheckList, verify=True, id=type_id):
        return type_checklist

    raise HTTPException(detail='Тип не найден', status_code=400)


def reformat_type_checklist_operations(types_check_list: dict) -> dict:

    typeCL_new = {
        'id': types_check_list['id'],
        'type_name': types_check_list['type_name']
    }

    typeCL_new_operations = []

    for operation in types_check_list['type_checklist_operations']:
        typeCL_new_operations.append(operation['operations'])

    typeCL_new['operations'] = typeCL_new_operations

    return typeCL_new


@router_type_checklist.get('/getAll')
async def get_all_type_checklist():

    types_check_list = await Query.get_all_data(model=TypeCheckList)

    return types_check_list


@router_type_checklist.post('')
async def insert_type_checklist(type_checklist=Depends(verify_type_checklist)):

    if await Query.insert_data(model=TypeCheckList, type_name=type_checklist.type_name):

        return JSONResponse(content={'message': 'Тип добавлен'}, status_code=201)

    return JSONResponse(content={'message': 'Произошла ошибка при добавлении типа'}, status_code=500)


@router_type_checklist.get('/{type_id}')
async def get_type_checklist(type_id: int):

    types_check_list = await Query.get_data_by_id(model=TypeCheckList, model_id=type_id)

    return types_check_list


@router_type_checklist.delete('/{type_id}')
async def delete_type_checklist(type_id: int):

    if await Query.delete_data(model=TypeCheckList, model_id=type_id):
        return JSONResponse(content={'message': 'Тип удален'}, status_code=200)

    return JSONResponse(content={'message': 'Произошла ошибка при удалении'}, status_code=500)


@router_type_checklist.patch('/{type_id}')
async def update_type_checklist(type_id: int, data=Depends(verify_update_type_checklist)):

    if await Query.update_date(model=TypeCheckList, model_id=type_id, **data.dict()):
        return JSONResponse(content={'message': 'Тип изменен'}, status_code=200)

    return JSONResponse(content={'message': 'Произошла ошибка при изменении'}, status_code=500)


# TODO доработать момент что если тип чек листа не существует - выдаем ошибку
@router_type_checklist.get('/{type_checklist_id}/create_template')
async def get_template_create(type_checklist_id: int):

    template = {

        'checklist': {
            'user_id': None,
            'type_id': type_checklist_id,
            'creation_time': None,
            "finish_time": None
        },

        'operations': [

        ]

    }

    type_with_operations = await get_operations_by_type(id_type=type_checklist_id)

    for operation in type_with_operations['operations']:

        if operation['status'] == 1:

            template['operations'].append({

                'operation_id': operation['id'],
                "working_before": None,
                "working_after": None,
                "comment": None

            })

    if not template['operations']:
        raise HTTPException(status_code=400, detail='Операции для данного типа не назначены')

    return template


@router_type_checklist.get('/all_by_operations', tags=['Type_checklist_operations'])
async def get_all_types_checklist_operations():

    types_check_list_by_operations = await Query.get_operations_by_all_type()

    typeCL_operations_new = []

    for typeCL in types_check_list_by_operations:

        typeCL_new = reformat_type_checklist_operations(typeCL)
        typeCL_operations_new.append(typeCL_new)

    return typeCL_operations_new


@router_type_checklist.get('/{id_type}/operations', tags=['Type_checklist_operations'])
async def get_operations_by_type(id_type: int):

    """
    Возвращает все операции с дополнительным полем status, которое отображает подключена операция или нет
    """

    operations = await Query.get_operations_by_type(type_id=id_type)

    return operations


@router_type_checklist.post('/operations/insert', tags=['Type_checklist_operations'])
async def insert_operation_in_type(data=Depends(verify_type_operation)):

    if await Query.insert_data(model=TypeCheckListOperations, type_id=data.type_id, operation_id=data.operation_id):
        return JSONResponse(content={'message': 'Операция добавлена'}, status_code=200)

    return JSONResponse(content={'message': 'Произошла ошибка'}, status_code=400)


@router_type_checklist.delete('/operations/delete', tags=['Type_checklist_operations'])
async def delete_operation_in_type(data=Depends(verify_type_operation)):

    if await Query.delete_data(model=TypeCheckListOperations, type_id=data.type_id, operation_id=data.operation_id):
        return JSONResponse(content={'message': 'Операция удалена из типа'})

    return JSONResponse(content={'message': 'Произошла ошибка при удалении операции'})

