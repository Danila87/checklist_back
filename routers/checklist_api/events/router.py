import datetime

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from database.Query import EventCrud

from pydentic_schemes import schemes

from misc import serializators

router_events = APIRouter(prefix='/events')


@router_events.get('/', tags=['events'])
async def get_events_for_month():
    result = await EventCrud.get_events_by_filter()

    return serializators.serialization_events(events=result)


@router_events.get('/by_interval/', tags=['events'])
async def get_events_by_interval(interval: int):
    sql_filter = f'WHERE DATE BETWEEN CURRENT_DATE AND CURRENT_DATE + {interval}'
    result = await EventCrud.get_events_by_filter(sql_add=sql_filter)

    return serializators.serialization_events(events=result)


@router_events.get('/by_date/', tags=['events'])
async def get_events_by_date(date_event: datetime.date):
    sql_filter = f"WHERE DATE = '{date_event}'"
    result = await EventCrud.get_events_by_filter(sql_add=sql_filter)

    return serializators.serialization_events(events=result)


@router_events.get('/{event_id}', tags=['events'])
async def get_event_by_id(event_id: int):

    result = await EventCrud.get_event_by_id(event_id=event_id)

    if not result:
        return None

    return serializators.serialization_event(event=result)


@router_events.post('/', tags=['events'])
async def create_event(event: schemes.Event):

    if isinstance(event.event_date, int):
        event.event_date = datetime.datetime.fromtimestamp(event.event_date).date()

    if await EventCrud.insert_event(event=event):
        return JSONResponse(content={"message": "Событие добавлено"}, status_code=201)

    return JSONResponse(content={"message": "Произошла ошибка при добавлении события"}, status_code=500)


@router_events.patch('/', tags=['events'])
async def update_event(event: schemes.EventUpdate):

    if await EventCrud.update_event(event=event):
        return JSONResponse(content={"message": 'Событие изменено'}, status_code=200)

    return JSONResponse(content={"message": 'Произошла ошибка при изменении'}, status_code=500)
