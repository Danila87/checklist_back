import datetime
import time

from typing import List

from pydantic import BaseModel, EmailStr, Field


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
