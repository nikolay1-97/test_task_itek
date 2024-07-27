"""Модуль со схемами данных запрсов и ответов."""
from pydantic import BaseModel

class UserModel(BaseModel):
    """Модель данных создания пользователя."""
    surname: str
    name: str
    patronymic: str


class UserUpdateResp(BaseModel):
    """Модель ответа обновления пользователя."""
    id: str
    new_surname: str
    new_name: str
    new_patronymic: str

class UserResp(BaseModel):
    """Модель ответа запроса пользователя."""
    id: str
    surname: str
    name: str
    patronymic: str


class UserRespRedis(BaseModel):
    """Модель ответа запроса пользователя."""
    id: str
    surname: str
    name: str
    patronymic: str


class UserUpdateRespRedis(BaseModel):
    """Модель ответа запроса пользователя."""
    id: str
    new_surname: str
    new_name: str
    new_patronymic: str
