import datetime


def serialization_event(event) -> dict:

    data = {
            "id": event.id,
            "event_title": event.event_title,
            "event_description": event.event_description,
            "is_active": event.is_active,
            "event_date": datetime.datetime.date(event.event_date),
            "user_id": event.rel_user.id,
            "user": {
                "id": event.rel_user.id,
                "username": event.rel_user.username
            }
        }

    if event.rel_schedule:
        data['schedule'] = {
            "event_id": event.rel_schedule[0].event_id,
            "day_interval": event.rel_schedule[0].day_interval,
            "id": event.rel_schedule[0].id
        }

    return data


def serialization_events(events) -> list[dict]:

    data = [{
        'id': event.id,
        'event_title': event.event_title,
        'event_description': event.event_description,
        'event_date': event.date,
        'user_username': event.username
    }
        for event in events
    ]

    return data
