"""Файл запуска приложения."""
from fastapi import FastAPI
from redis import asyncio as aioredis
import uvicorn

from config import settings

from views.crud_for_users import user_router


def get_application() -> FastAPI:
    """Возвращает экземпляр приложения."""
    application = FastAPI()
    return application

application = get_application()

application.include_router(user_router)

if __name__ == '__main__':
    uvicorn.run(
        app=application,
        host=settings.app_host,
        port=int(settings.app_port),
    )