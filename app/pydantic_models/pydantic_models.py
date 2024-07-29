"""Модуль со схемами данных."""
from pydantic import BaseModel

class UserModel(BaseModel):
    """Модель данных для создания пользователя."""
    surname: str
    name: str
    patronymic: str


class UserUpdateResp(BaseModel):
    """Модель данных ответа для обновления пользователя."""
    id: str
    new_surname: str
    new_name: str
    new_patronymic: str


class UserResp(BaseModel):
    """Модель данных ответа для запроса пользователя."""
    id: str
    surname: str
    name: str
    patronymic: str
