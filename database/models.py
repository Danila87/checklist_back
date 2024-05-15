import asyncio

from sqlalchemy import Column, String, Integer, Boolean, Time, ForeignKey, select, Date, UniqueConstraint, Table, DateTime, LargeBinary, TIMESTAMP
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.exc import NoResultFound
from .connection import db_session
from fastapi.encoders import jsonable_encoder
from datetime import datetime


class Base(DeclarativeBase):
    pass


class User(Base):

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)

    username = Column(String(100), unique=True)
    email = Column(String(320), unique=True)
    hashed_password = Column(LargeBinary(1024))

    is_superuser = Column(Boolean, default=False, nullable=False)

    checklists = relationship('CheckList', back_populates='user')


class CheckList(Base):

    __tablename__ = 'checklists'

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey('users.id'))
    type_id = Column(Integer, ForeignKey('type_checklist.id'))

    creation_time = Column(DateTime)
    finish_time = Column(DateTime)

    user = relationship('User', back_populates='checklists')
    type = relationship('TypeCheckList', back_populates='checklists')
    checklists_operations = relationship('CheckListOperations', back_populates='checklists')


class CheckListOperations(Base):

    __tablename__ = 'checklist_operations'

    id = Column(Integer, primary_key=True)

    checklist_id = Column(Integer, ForeignKey('checklists.id'))
    operation_id = Column(Integer, ForeignKey('operations.id'))

    working_before = Column(String(100))
    working_after = Column(String(100))

    comment = Column(String(500))

    checklists = relationship('CheckList', back_populates='checklists_operations')
    operations = relationship('Operation', back_populates='checklists')


class TypeCheckList(Base):

    __tablename__ = 'type_checklist'

    id = Column(Integer, primary_key=True)
    type_name = Column(String(100), unique=True)

    checklists = relationship('CheckList', back_populates='type')
    type_checklist_operations = relationship('TypeCheckListOperations', back_populates='types', cascade='all, delete-orphan')


class Operation(Base):

    __tablename__ = 'operations'

    id = Column(Integer, primary_key=True)

    name_operation = Column(String(100))
    hint = Column(String(500), nullable=True)

    checklists = relationship('CheckListOperations', back_populates='operations')
    type_checklist_operations = relationship('TypeCheckListOperations', back_populates='operations', cascade='all, delete-orphan')


class TypeCheckListOperations(Base):

    __tablename__ = 'type_checklist_operations'
    __table_args__ = (
        UniqueConstraint('type_id', 'operation_id', name='idx_unique_type_operations'),
    )
    id = Column(Integer, primary_key=True)

    type_id = Column(Integer, ForeignKey('type_checklist.id'))
    operation_id = Column(Integer, ForeignKey('operations.id'))

    types = relationship('TypeCheckList', back_populates='type_checklist_operations')
    operations = relationship('Operation', back_populates='type_checklist_operations')
