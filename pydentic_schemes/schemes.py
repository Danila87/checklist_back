import datetime
import time

from typing import List

from pydantic import BaseModel, EmailStr, Field, field_validator


class Operation(BaseModel):
    name_operation: str
    hint: str | None = None


class TypeCheckList(BaseModel):
    type_name: str


class TypeCheckListOperations(BaseModel):
    type_id: int
    operation_id: int


class CheckListInsert(BaseModel):
    user_id: int
    type_id: int

    creation_time: int  # unix time
    finish_time: int  # unix time


class CheckListOperationsInsert(BaseModel):
    operation_id: int
    working_before: str
    working_after: str
    comment: str | None = None


class CheckListCreate(BaseModel):
    checklist: CheckListInsert
    operations: List[CheckListOperationsInsert]


class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str | bytes


class UserLogin(BaseModel):
    login: str
    password: str


class Test(BaseModel):
    creation_time: int


class EventSchedule(BaseModel):
    day_interval: int = 1

    @field_validator('day_interval')
    @classmethod
    def valid_interval(cls, day_interval):

        if day_interval <= 0:
            raise ValueError('Недопустимый интервал')

        return day_interval


class Event(BaseModel):
    event_title: str
    event_description: str | None = None
    event_date: datetime.date

    is_active: int = 1

    user_id: int

    schedule: EventSchedule | None = None

    @field_validator('is_active')
    @classmethod
    def valid_active(cls, is_active):
        if is_active not in (0, 1):
            raise ValueError('Неверный статус у is_active')

        return is_active
