import datetime

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from database.Query import EventCrud

from pydentic_schemes import schemes

router_events = APIRouter(prefix='/events')


@router_events.get('/', tags=['events'])
async def get_events_for_month():
    result = await EventCrud.get_events_by_filter()

    return [{
        'id': row.id,
        'event_title': row.event_title,
        'event_description': row.event_description,
        'event_date': row.date
    }
        for row in result
    ]


@router_events.get('/by_interval/', tags=['events'])
async def get_events_by_interval(interval: int):
    sql_filter = f'WHERE DATE BETWEEN CURRENT_DATE AND CURRENT_DATE + {interval}'
    result = await EventCrud.get_events_by_filter(sql_add=sql_filter)

    return [{
        'id': row.id,
        'event_title': row.event_title,
        'event_description': row.event_description,
        'event_date': row.date
    }
        for row in result
    ]


@router_events.get('/by_date/', tags=['events'])
async def get_events_by_date(date_event: datetime.date):
    sql_filter = f"WHERE DATE = '{date_event}'"
    result = await EventCrud.get_events_by_filter(sql_add=sql_filter)

    return [{
        'id': row.id,
        'event_title': row.event_title,
        'event_description': row.event_description,
        'event_date': row.date
    }
        for row in result
    ]


@router_events.get('/{event_id}', tags=['events'])
async def get_event_by_id(event_id: int):
    result = await EventCrud.get_event_by_id(event_id=event_id)

    data = {
        "id": result.id,
        "event_title": result.event_title,
        "event_description": result.event_description,
        "is_active": result.is_active,
        "event_date": datetime.datetime.date(result.event_date),
        "user": {
            "id": result.rel_user.id,
            "username": result.rel_user.username
        }
    }

    if result.rel_schedule:
        data['schedule'] = {
            "event_id": result.rel_schedule[0].event_id,
            "day_interval": result.rel_schedule[0].day_interval,
            "id": result.rel_schedule[0].id
        }

    return data


@router_events.post('/', tags=['events'])
async def create_event(event: schemes.Event):
    if isinstance(event.event_date, int):
        event.event_date = datetime.datetime.fromtimestamp(event.event_date).date()

    if await EventCrud.insert_event(event=event):
        return JSONResponse(content={"message": "Событие добавлено"}, status_code=201)

    return JSONResponse(content={"message": "Произошла ошибка при добавлении события"}, status_code=500)


@router_events.put('/{event_id}')
async def update_event(event_id: int):
    pass
