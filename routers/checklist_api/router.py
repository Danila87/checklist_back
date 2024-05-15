from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from database.models import CheckList, Operation, CheckListOperations, TypeCheckList, TypeCheckListOperations
from database.Query import Query

from .operations.router import router_operations
from .types_checklist.router import router_type_checklist

from pydentic_schemes import schemes


router_checklist = APIRouter(prefix='/checklist')

router_checklist.include_router(
    router_operations,
)

router_checklist.include_router(
    router_type_checklist,
)


@router_checklist.get('/', tags=['checklist'])
async def get_checklists():

    # checklists = await Query.get_all_data(model=CheckList)

    checklists = await Query.get_all_checklists()
    return checklists


@router_checklist.get('/{id_checklist}', tags=['checklist'])
async def get_checklist(checklist_id: int):

    checklist = await Query.get_full_data_checklist(checklist_id=checklist_id)
    return checklist


@router_checklist.post('/', tags=['checklist'])
async def create_checklist(checklist_data: schemes.CheckListCreate):

    if await Query.checklist_transactions(checklist_data=checklist_data):
        return JSONResponse(content={"message": "Чек лист создан"}, status_code=201)

    return JSONResponse(content={"message": "Чек лист не создан"}, status_code=400)



