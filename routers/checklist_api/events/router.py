import datetime

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from database.Query import EventCrud

from pydentic_schemes import schemes

router_events = APIRouter(prefix='/events')


@router_events.get('/', tags=['events'])
async def get_events_for_month():
    return await EventCrud.get_events_by_filter()


@router_events.get('/by_interval/', tags=['events'])
async def get_events_by_interval(interval: int):
    sql_filter = f'WHERE DATE BETWEEN CURRENT_DATE AND CURRENT_DATE + {interval}'
    events = await EventCrud.get_events_by_filter(sql_add=sql_filter)

    return events


@router_events.get('/by_date/', tags=['events'])
async def get_events_by_date(date_event: datetime.date):
    sql_filter = f"WHERE DATE = '{date_event}'"
    events = await EventCrud.get_events_by_filter(sql_add=sql_filter)

    return events


@router_events.get('/{event_id}', tags=['events'])
async def get_event_by_id(event_id: int):
    return await EventCrud.get_event_by_id(event_id=event_id)


@router_events.post('/', tags=['events'])
async def create_event(event: schemes.Event):

    if await EventCrud.insert_event(event=event):
        return JSONResponse(content={"message": "Событие добавлено"}, status_code=201)

    return JSONResponse(content={"message": "Произошла ошибка при добавлении события"}, status_code=500)


@router_events.put('/{event_id}')
async def update_event():
    return 123