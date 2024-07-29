"""Модуль содержит классы-репозитории с использованием SQL и
NoSQL СУБД.

"""
import uuid

from fastapi import HTTPException
from starlette import status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from pydantic_models.pydantic_models import (
    UserUpdateResp,
    UserResp,
)
from data_sources.models import User_model
from config import settings, redis_instance


class UserRepository():
    """Базовый класс для создания репозиториев.

    Methods
    -------
    __init__()
        Инициализотор класа.

    create_user()
        Добавляет нового пользователя в бд.

    get_user()
        Возвращает пользователя.

    update_user()
        Обновляет данные пользователя.

    delete_user()
        Удаляет пользователя.
    """

    def __init__(
        self,
        create: bool,
        update: bool,
        read: bool,
        delete: bool,
    ):
        """Инициализатор класса.

        Parameters
        ----------
        create: bool
            Разрешение на добавление данных.
        update: bool
            Разрешение на обновление данных.
        read: bool
            Разрешение на чтение данных.
        delete: bool
            Разрешение на удаление данных.
        """

        self.create = create
        self.update = update
        self.read = read
        self.delete = delete

    async def create_user(self):
        pass
    
    async def get_user(self):
        pass
    
    async def update_user(self):
        pass
    
    async def delete_user(self):
        pass


class UserRepositorySQL(UserRepository):
    """Класс совершает CRUD операции с сущностью
    пользователь с
    использованием реляционной СУБД.
    
    Methods
    -------
    get_user_by_id()
        Возвращает пользователя по id.
    
    create_user()
        Создает нового пользователя.
    
    update_user()
        Обновляет данные пользователя.

    get_user()
        Возвращает пользователя по id.

    delete_user()
        Удаляет пользователя.

    """

    @classmethod
    async def get_user_by_id(
        cls, user_id: str,
        session: AsyncSession,
    ):
        """Возвращает пользователя по id.

        Parameters
        ----------
        user_id: str
            id пользователя.
            
        session: AsyncSession
            Сессия соединения с базой данных.
        """

        try:
            query = select(User_model).where(User_model.c.id == uuid.UUID(user_id))
            exists_user = await session.execute(query)
            exists_user = exists_user.all()
            if len(exists_user) > 0:
                return exists_user[0]
            return False
        except Exception as some_ex:
            print(some_ex)
            return False

    async def create_user(
        self,
        surname: str,
        name: str,
        patronymic: str,
        session: AsyncSession,
    ):
        """Создает нового пользователя.

        Parameters
        ----------
        surname: str
            Фамилия пользователя.

        name: str
            Имя пользователя.
        
        patronymic: str
            Отчество пользователя.
            
        session: AsyncSession
            Сессия соединения с базой данных.
        """

        if not self.create:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Добавление данных запрещено",
            )
        try:
            user_id = uuid.uuid4()
            query = User_model.insert().values(
                id=user_id,
                surname=surname,
                name=name,
                patronymic=patronymic,
            )
            await session.execute(query)
            await session.commit()
            user = await UserRepositorySQL.get_user_by_id(str(user_id), session)
            return UserResp(
                id = str(user[0]),
                surname = user[1],
                name = user[2],
                patronymic = user[3],
            )
        except Exception as some_ex:
            await session.rollback()
            print(some_ex)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail='Ошибка на стороне сервера',
            )
        
    async def update_user(
        self,
        surname: str,
        name: str,
        patronymic: str,
        user_id: str,
        session: AsyncSession,
    ):
        """Обновляет данные пользователя.

        Parameters
        ----------
        surname: str
            Фамилия пользователя.

        name: str
            Имя пользователя.
        
        patronymic: str
            Отчество пользователя.

        user_id: str
            id пользователя.
            
        session: AsyncSession
            Сессия соединения с базой данных.
        """

        if not self.update:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Обновление данных запрещено",
            )
        exists_user = await UserRepositorySQL.get_user_by_id(user_id, session)

        if exists_user:
            try:
                query = User_model.update().where(
                    User_model.c.id == uuid.UUID(user_id),
                ).values(
                    surname=surname,
                    name=name,
                    patronymic=patronymic,
                )
                await session.execute(query)
                await session.commit()
                user = await UserRepositorySQL.get_user_by_id(user_id, session)
                return UserUpdateResp(
                    id=str(user[0]),
                    new_surname=user[1],
                    new_name=user[2],
                    new_patronymic=user[3],
                )
            except Exception as some_ex:
                await session.rollback()
                print(some_ex)
                raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail='Ошибка на стороне сервера',
                )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Пользователь не найден",
            )
        
    async def get_user(self, user_id: str, session: AsyncSession):
        """Возвращает пользователя по id.

        Parameters
        ----------
        user_id: str
            id пользователя.
            
        session: AsyncSession
            Сессия соединения с базой данных.
        """

        if not self.read:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Чтение данных запрещено",
            )
        user = await UserRepositorySQL.get_user_by_id(user_id, session)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Пользователь не найден',
            )
        try:
            return UserResp(
                id=str(user[0]),
                surname=user[1],
                name=user[2],
                patronymic=user[3],
            )
        except Exception as some_ex:
            print(some_ex)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail='Ошибка на стороне сервера',
            )
        
    async def delete_user(self, user_id: str, session: AsyncSession):
        """Удаляет пользователя по id.

        Parameters
        ----------
        user_id: str
            id пользователя.

        session: AsyncSession
            Сессия соединения с базой данных.
        """

        if not self.delete:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Удаление данных запрещено",
            )
        exists_user = await UserRepositorySQL.get_user_by_id(user_id, session)
        if not exists_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Пользователь не найден',
            )
        try:
            query = User_model.delete().where(User_model.c.id == uuid.UUID(user_id))
            await session.execute(query)
            await session.commit()
            return {
                "status": True,
                "message": "Пользователь успешно удален"
            }
        except Exception as some_ex:
            await session.rollback()
            print(some_ex)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail='Ошибка на стороне сервера',
            )
        

class UserRepositoryNoSQL(UserRepository):
    """Класс совершает CRUD операции с сущностью
    пользователь с
    использованием NoSQL СУБД.

    Attributes
    ----------
    REDIS_INSTANCE : Redis
        экземпляр редис
    
    Methods
    -------
    get_user_by_id()
        Возвращает пользователя по id.
    
    create_user()
        Создает нового пользователя.
    
    update_user()
        Обновляет данные пользователя.

    get_user()
        Возвращает пользователя по id.

    delete_user()
        Удаляет пользователя.

    """

    REDIS_INSTANCE = redis_instance

    @classmethod
    async def get_user_by_id(cls, user_id: str):
        """Возвращает пользователя по id.

        Parameters
        ----------
        user_id: str
            id пользователя.
            
        """

        try:
            user = await cls.REDIS_INSTANCE.hgetall(user_id)
            if user:
                return user
            return False
        except Exception as some_ex:
            print(some_ex)
            return False
        
    async def get_user(self, user_id: str):
        """Возвращает пользователя по id.

        Parameters
        ----------
        user_id: str
            id пользователя.
            
        """

        if not self.read:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Чтение данных запрещено",
            )
        user = await UserRepositoryNoSQL.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Пользователь не найден',
            )
        try:
            return UserResp(
                id = user['id'],
                surname = user['surname'],
                name = user['name'],
                patronymic = user['patronymic'],
            )
        except Exception as some_ex:
            print(some_ex)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail='Ошибка на стороне сервера',
            )

    async def create_user(
        self,
        surname: str,
        name: str,
        patronymic: str,
    ):
        """Создает нового пользователя.

        Parameters
        ----------
        surname: str
            Фамилия пользователя.

        name: str
            Имя пользователя.
        
        patronymic: str
            Отчество пользователя.
        """

        if not self.create:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Добавление данных запрещено",
            )
        try:
            user_id = str(uuid.uuid4())
            pipeline = await UserRepositoryNoSQL.REDIS_INSTANCE.pipeline(
                transaction=True,
            )
            await pipeline.hmset(
                user_id,
                {   'id': user_id,
                    'surname': surname,
                    'name': name,
                    'patronymic': patronymic,
                }
            )
            await pipeline.execute()
            user = await UserRepositoryNoSQL.REDIS_INSTANCE.hgetall(user_id)
            return UserResp(
                id = user['id'],
                surname = user['surname'],
                name = user['name'],
                patronymic = user['patronymic'],
            )
        except Exception as some_ex:
            await pipeline.discard()
            print(some_ex)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail='Ошибка на стороне сервера',
            )

    async def update_user(
        self,
        surname: str,
        name: str,
        patronymic: str,
        user_id: str,
    ):
        """Обновляет данные пользователя.

        Parameters
        ----------
        surname: str
            Фамилия пользователя.

        name: str
            Имя пользователя.
        
        patronymic: str
            Отчество пользователя.

        user_id: str
            id пользователя.
        """

        if not self.update:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Обновление данных запрещено",
            )
        user = await UserRepositoryNoSQL.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Пользователь не найден',
            )
        try:
            pipeline = await UserRepositoryNoSQL.REDIS_INSTANCE.pipeline(
                transaction=True,
            )
            await pipeline.hmset(
                user_id,
                {   'id': user_id,
                    'surname': surname,
                    'name': name,
                    'patronymic': patronymic,
                }
            )
            await pipeline.execute()
            user = await UserRepositoryNoSQL.REDIS_INSTANCE.hgetall(user_id)
            return UserUpdateResp(
                id = user['id'],
                new_surname = user['surname'],
                new_name = user['name'],
                new_patronymic = user['patronymic'],
            )
        except Exception as some_ex:
            await pipeline.discard()
            print(some_ex)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail='Ошибка на стороне сервера',
            )

    async def delete_user(self, user_id: str):
        """Удаляет пользователя по id.

        Parameters
        ----------
        user_id: str
            id пользователя.
        """
        
        if not self.delete:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Удаление данных запрещено",
            )
        user = await UserRepositoryNoSQL.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Пользователь не найден',
            )
        try:
            pipeline = await UserRepositoryNoSQL.REDIS_INSTANCE.pipeline(
                transaction=True,
            )
            await pipeline.delete(user_id)
            await pipeline.execute()
            return {
                "status": True,
                "message": "Пользователь успешно удален"
            }
        except Exception as some_ex:
            await pipeline.discard()
            print(some_ex)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail='Ошибка на стороне сервера',
            )
 
#Если значение переменной окружение NO_SQL = True,
#создается экземпляр репозитория с использованием нереляционной СУБД.
#Если значение переменной окружение NO_SQL = False,
#создается экземпляр репозитория с использованием реляционной СУБД.
if settings.no_sql:
    user_repository = UserRepositoryNoSQL(
        settings.create,
        settings.update,
        settings.read,
        settings.delete,
    )
else:
    user_repository = UserRepositorySQL(
        settings.create,
        settings.update,
        settings.read,
        settings.delete,
    )
