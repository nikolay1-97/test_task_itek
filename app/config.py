"""Модуль содержит конфигурацию работы приложения."""
import os

from starlette.config import Config
from pydantic_settings import BaseSettings, SettingsConfigDict
from redis import asyncio as aioredis


dir_path = os.path.dirname(os.path.realpath(__file__))
root_dir = dir_path[:-3]
config = Config(f'{root_dir}.env')

DB_USER = config('DB_USER', cast=str)
PASSWORD = config('PASSWORD', cast=str)
DB_HOST = config('DB_HOST', cast=str)
DB_PORT = config('DB_PORT', cast=str)
DB_NAME = config('DB_NAME', cast=str)

PATH_TO_ENV_FILE = root_dir + '.env'

class Settings(BaseSettings):
    """Класс содержит конфигурацию работы приложения.

    Attributes
    ----------
    db_user: str
        имя пользователя базы данных
    password: str
        пароль базы данных
    db_host: str
        хост базы данных
    db_port: str
        порт базы данныз
    db_name: str
        имя базы данных
    redis_host: str
        хост для redis
    redis_port: str
        порт для redis
    app_host: str
        хост для запуска приложения
    app_port: str
        порт для запуска приложения
    no_sql: bool
        выбор типа репозитория
    create: bool
        разрешение на добавление данных
    update: bool
        разрешение на обновление данных
    read: bool
        разрешение на чтение данных
    delete: bool
        разрешение на удаление данных

    """

    db_user: str
    password: str
    db_host: str
    db_port: str
    db_name: str
    redis_host: str
    redis_port: str
    app_host: str
    app_port: str
    no_sql: bool
    create: bool
    update: bool
    read: bool
    delete: bool
    model_config = SettingsConfigDict(
        env_file='.env', extra='ignore', env_file_encoding='utf-8')


settings = Settings(
    _env_file=PATH_TO_ENV_FILE,
    extra='ignore',
    env_file_encoding='utf-8',
)

DB_URL = f'postgresql+asyncpg://{settings.db_user}:{settings.password}@{settings.db_host}:{settings.db_port}/{settings.db_name}'

redis_instance = aioredis.from_url(
        f"redis://{settings.redis_host}:{settings.redis_port}",
        encoding="utf8",
        decode_responses=True,
)
