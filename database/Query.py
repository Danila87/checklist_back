import datetime
from typing import Type

from sqlalchemy.exc import NoResultFound
from sqlalchemy import select, update, case

from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException

from sqlalchemy.orm import joinedload, selectinload

from .connection import db_session
from .models import User, CheckList, CheckListOperations, Operation, TypeCheckListOperations, TypeCheckList


class Query:

    @staticmethod
    async def get_all_data(model) -> list[dict]:

        async with db_session() as session:
            query = select(model).order_by(model.id)
            query_result = await session.execute(query)
            data = query_result.scalars().all()

            return jsonable_encoder(data)

    @staticmethod
    async def get_data_by_id(model, model_id, verify: bool = False, encode: bool = True) -> dict | Type[
        NoResultFound] | bool:

        async with db_session() as session:
            query = select(model).filter(model.id == model_id)
            query_result = await session.execute(query)

            data = query_result.scalar_one_or_none()

            if verify:

                if data:
                    return True

                return False

            if not data:
                raise HTTPException(detail='Пустой результат', status_code=400)

            if encode:
                return jsonable_encoder(data)

            return data

    @staticmethod
    async def get_data_by_filter(model, verify: bool = False, encode: bool = True, **kwargs) -> list[dict] | bool:

        async with db_session() as session:

            query = select(model).filter_by(**kwargs)
            query_result = await session.execute(query)
            data = query_result.scalars().all()

            if verify:
                if len(data) > 0:
                    return True

                return False

            if encode:
                return jsonable_encoder(data)

            return data

    @staticmethod
    async def insert_data(model, **kwargs) -> bool:
        async with db_session() as session:
            data = model(**kwargs)
            session.add(data)
            await session.commit()

            return True

    @staticmethod
    async def delete_data(model, model_id: int = None, **kwargs) -> bool:

        async with db_session() as session:

            if kwargs:
                data = await Query.get_data_by_filter(model=model, encode=False, **kwargs)
            else:
                data = await Query.get_data_by_id(model=model, model_id=model_id, encode=False)

            try:

                if isinstance(data, list):

                    for i in data:
                        print(i)
                        await session.delete(i)


                else:

                    await session.delete(data)

                await session.commit()

                return True

            except:
                return False

    @staticmethod
    async def update_date(model, model_id: int, **kwargs) -> bool:

        async with db_session() as session:

            try:
                query = update(model).where(model.id == model_id).values(**kwargs)
                query_result = await session.execute(query)
                await session.commit()

                return True

            except:
                return False

    @staticmethod
    async def get_all_checklists() -> list[dict]:

        async with db_session() as session:
            query = select(CheckList).options(selectinload(CheckList.user)).options(selectinload(CheckList.type))
            query_result = await session.execute(query)

            data = query_result.scalars().all()

            all_checklists = [{
                'id': checklist.id,
                'type': checklist.type.type_name,
                'user': checklist.user.username,
                'creation_time': checklist.creation_time,
                'finish_time': checklist.finish_time
            }
                for checklist in data
            ]

            return all_checklists

    @staticmethod
    async def checklist_transactions(checklist_data) -> bool:

        async with db_session() as session:
            async with session.begin():
                checklist = dict(checklist_data.checklist)
                operations = [dict(operation) for operation in checklist_data.operations]

                checklist['creation_time'] = datetime.datetime.fromtimestamp(timestamp=checklist['creation_time'])
                checklist['finish_time'] = datetime.datetime.fromtimestamp(timestamp=checklist['finish_time'])

                data_checklist = CheckList(**dict(checklist))

                session.add(data_checklist)

                await session.flush()
                await session.refresh(data_checklist)

                for operation in operations:
                    operation['checklist_id'] = data_checklist.id

                    data_operation = CheckListOperations(**operation)
                    session.add(data_operation)

                await session.flush()

                return True

                # except:
                #     await session.rollback()
                #     return False

    @staticmethod
    async def get_full_data_checklist(checklist_id: int):

        async with db_session() as session:
            query = select(CheckList).options(
                selectinload(CheckList.checklists_operations).joinedload(CheckListOperations.operations)
            ).options(
                joinedload(CheckList.user)
            ).options(
                joinedload(CheckList.type)
            ).where(CheckList.id == checklist_id)

            query_result = await session.execute(query)
            data = query_result.scalar_one_or_none()

            checklist_data = {

                'checklist': {
                    'id': checklist_id,
                    'type_checklist': data.type.type_name,
                    "creation_time": data.creation_time,
                    "finish_time": data.finish_time,
                },

                'user': {
                    'id': data.user.id,
                    'username': data.user.username
                },

                'operations': [
                    {
                        'id': operation.operations.id,
                        'name_operation': operation.operations.name_operation,
                        'hint': operation.operations.hint,
                        'working_before': operation.working_before,
                        'working_after': operation.working_after,
                        'comment': operation.comment,
                    }
                    for operation in data.checklists_operations
                ]

            }

            return checklist_data

    @staticmethod
    async def get_operations_by_type(type_id: int):

        async with db_session() as session:
            subquery = select(TypeCheckListOperations.operation_id).where(
                TypeCheckListOperations.type_id == type_id).correlate(None).as_scalar()

            query = select(
                Operation.id,
                Operation.name_operation,
                Operation.hint,
                case(
                    (Operation.id.in_(subquery), 1),
                    else_=0
                ).label('status'))

            query_result = await session.execute(query)
            operations = [{"id": row.id, "name_operation": row.name_operation, "hint": row.hint, "status": row.status}
                          for row in query_result]

        type_checklist_with_operations = await Query.get_data_by_id(model=TypeCheckList, model_id=type_id)
        type_checklist_with_operations['operations'] = operations

        return type_checklist_with_operations

    @staticmethod
    async def get_operations_by_all_type():

        async with db_session() as session:
            query = select(TypeCheckList).options(
                selectinload(TypeCheckList.type_checklist_operations).joinedload(TypeCheckListOperations.operations))
            data = await session.scalars(query)

            return jsonable_encoder(data.all())

    @staticmethod
    async def insert_operation_in_type(**kwargs):

        async with db_session() as session:
            data = CheckListOperations(**kwargs)
            session.add(data)
            await session.commit()

            return True


# TODO заготовка под разделение класса Query
"""
class BaseQuery:

    @staticmethod
    async def get_all_data(model) -> list[dict]:

        async with db_session() as session:
            query = select(model)
            query_result = await session.execute(query)
            data = query_result.scalars().all()

            return jsonable_encoder(data)

    @staticmethod
    async def get_data_by_id(model, model_id, verify: bool = False, encode: bool = True) -> dict | Type[
        NoResultFound] | bool:

        async with db_session() as session:
            query = select(model).filter(model.id == model_id)
            query_result = await session.execute(query)

            data = query_result.scalar_one_or_none()

            if verify:

                if data:
                    return True

                return False

            if not data:
                raise HTTPException(detail='Пустой результат', status_code=400)

            if encode:
                return jsonable_encoder(data)

            return data

    @staticmethod
    async def get_data_by_filter(model, verify: bool = False, encode: bool = True, **kwargs) -> list[dict] | bool:

        async with db_session() as session:

            query = select(model).filter_by(**kwargs)
            query_result = await session.execute(query)
            data = query_result.scalars().all()

            if verify:
                if len(data) > 0:
                    return True

                return False

            if encode:
                return jsonable_encoder(data)

            return data

    @staticmethod
    async def insert_data(model, **kwargs) -> bool:
        async with db_session() as session:
            data = model(**kwargs)
            session.add(data)
            await session.commit()

            return True

    @staticmethod
    async def delete_data(model, model_id: int = None, **kwargs) -> bool:

        async with db_session() as session:

            if kwargs:
                data = await Query.get_data_by_filter(model=model, encode=False, **kwargs)
            else:
                data = await Query.get_data_by_id(model=model, model_id=model_id, encode=False)

            try:

                if isinstance(data, list):

                    for i in data:
                        print(i)
                        await session.delete(i)


                else:

                    await session.delete(data)

                await session.commit()

                return True

            except:

                return False

    @staticmethod
    async def update_date(model, model_id: int, **kwargs) -> bool:
        pass
"""
