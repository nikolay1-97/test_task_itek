"""Модуль с моделями данных базы данных."""
import uuid

from sqlalchemy import (
    MetaData,
    Table,
    Column,
    String,
)
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.dialects.postgresql import UUID

from config import DB_URL


metadata = MetaData()

engine = create_async_engine(DB_URL)

async_session_maker = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_async_session():
    async with async_session_maker() as session:
        yield session

#Модель данных для сущности пользователь.
User_model = Table(
    "user",
    metadata,
    Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True),
    Column('surname', String, nullable=False),
    Column('name', String, nullable=False),
    Column('patronymic', String, nullable=False),
)
