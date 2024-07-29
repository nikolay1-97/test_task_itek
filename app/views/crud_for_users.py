"""Модуль с функциями-обработчиками запросов."""
from fastapi import APIRouter, Depends
from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession

from data_sources.models import get_async_session
from pydantic_models.pydantic_models import UserModel
from data_sources.storages.user_repository import user_repository
from config import settings

user_router = APIRouter()

@user_router.post('/api/v1/users')
async def create_user(
    request: UserModel,
    session: AsyncSession = Depends(get_async_session),
):
    """Запрос на создание нового пользователя.

    Parameters
    ----------
    request: UserModel
        Данные запроса.
        
    session: AsyncSession
        Сессия соединения с базой данных.
    """
    if settings.no_sql:
        return await user_repository.create_user(
            request.surname,
            request.name,
            request.patronymic,
        )
    return await user_repository.create_user(
        request.surname,
        request.name,
        request.patronymic,
        session,
    )


@user_router.patch('/api/v1/users/{target_user_id}')
async def update_user(
    request: UserModel,
    target_user_id: str,
    session: AsyncSession = Depends(get_async_session),
):
    """Запрос на обновление данных пользователя.

    Parameters
    ----------
    requests: UserModel
        Данные запроса.
        
    target_user_id: str
        id пользователя.

    session: AsyncSession
        Сессия соединения с базой данных.
    """
    if settings.no_sql:
        return await user_repository.update_user(
            request.surname,
            request.name,
            request.patronymic,
            target_user_id,
        )
    return await user_repository.update_user(
        request.surname,
        request.name,
        request.patronymic,
        target_user_id,
        session)


@user_router.get('/api/v1/users/{user_id}')
async def get_user(
    request: Request,
    user_id: str,
    session: AsyncSession = Depends(get_async_session),
):
    """Запрос на получение данных пользователя.

    Parameters
    ----------
    requests: Request
        Объект Request.

    user_id: str
        id пользователя

    session: AsyncSession
        Сессия соединения с базой данных.
    """
    if settings.no_sql:
        return await user_repository.get_user(user_id)
    return await user_repository.get_user(user_id, session)


@user_router.delete('/api/v1/users/{user_id}')
async def delete_user(
    request: Request,
    user_id: str,
    session: AsyncSession = Depends(get_async_session),
):
    """Запрос на удаление пользователя.

    Parameters
    ----------
    requests: Request
        Объект Request.

    user_id: str
        id пользователя

    session: AsyncSession
        Сессия соединения с базой данных.
    """
    if settings.no_sql:
        return await user_repository.delete_user(user_id)
    return await user_repository.delete_user(user_id, session)
