import uuid

from fastapi import HTTPException
from starlette import status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from pydantic_models.pydantic_models import UserUpdateResp, UserModel, UserResp, UserRespRedis, UserUpdateRespRedis
from data_sources.models import User_model
from config import settings, redis_instance


class UserRepository():

    def __init__(
        self,
        create,
        update,
        read,
        delete,
    ):
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


class UserRepositoryPostgre(UserRepository):

    @classmethod
    async def get_user_by_id(cls, user_id: str, session: AsyncSession):
        """Возвращает объект пользователь по id.

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
                return exists_user
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
        if self.create != 'True':
            return 'Добавление данных запрещено'
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
            user = await UserRepositoryPostgre.get_user_by_id(str(user_id), session)
            return UserResp(
                id = str(user[0][0]),
                surname = user[0][1],
                name = user[0][2],
                patronymic = user[0][3],
            )
        except Exception as some_ex:
            await session.rollback()
            print(some_ex)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        
    async def get_users_list(self, session: AsyncSession):
        """Возвращает список пользователей.

        Parameters
        ----------
        session: str
            Сессия соединения с базой данных.
        """
        if not self.read:
            return 'Чтение данных запрещено'
        try:
            query = select(User_model)
            users_list = await session.execute(query)
            users_list = users_list.all()
            if len(users_list) == 0:
                return {}
            response = {}

            for i in range(len(users_list)):
                response[users_list[i][0]] = {
                    "id": users_list[i][0],
                    "surname": users_list[i][1],
                    "name": users_list[i][2],
                    "patronymic": users_list[i][3],
                }
            return response
        except Exception as some_ex:
            print(some_ex)
            return {'message': 'Ошибка на стороне сервера'}
        
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
        name: str
            Имя пользователя.
        surname: str
            Фамилия пользователя.
        email: str
            email пользователя..
        role: int
            id роли пользователя.
        session: AsyncSession
            Сессия соединения с базой данных.
        """
        if self.update != 'True':
            return 'Обновление данных запрещено'
        exists_user = await UserRepositoryPostgre.get_user_by_id(user_id, session)

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
                user = await UserRepositoryPostgre.get_user_by_id(user_id, session)
                return UserUpdateResp(
                    id=str(user[0][0]),
                    new_surname=user[0][1],
                    new_name=user[0][2],
                    new_patronymic=user[0][3],
                )

            except Exception as some_ex:
                await session.rollback()
                print(some_ex)
                raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Пользователь не найден",
            )
        
    async def get_user(self, user_id: str, session: AsyncSession):
        if self.read != 'True':
            return 'Чтение данных запрещено'
        user = await UserRepositoryPostgre.get_user_by_id(user_id, session)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Пользователь не найден',
            )
        try:
            return UserResp(
                id=str(user[0][0]),
                surname=user[0][1],
                name=user[0][2],
                patronymic=user[0][3],
            )
        except Exception as some_ex:
            print(some_ex)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        

    async def delete_user(self, user_id: str, session: AsyncSession):
        """Удаляет пользователя по id.

        Parameters
        ----------
        target_user_id: str
            id пользователя.
        session: AsyncSession
            Сессия соединения с базой данных.
        """
        if self.delete != 'True':
            return 'Удаление данных запрещено'
        exists_user = await UserRepositoryPostgre.get_user_by_id(user_id, session)
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
            )
        

class UserRepositoryRedis(UserRepository):

    REDIS_INSTANCE = redis_instance

    @classmethod
    async def get_user_by_id(cls, user_id: str):
        try:
            user = await cls.REDIS_INSTANCE.hgetall(user_id)
            if user:
                return user
            return False
        except Exception as some_ex:
            print(some_ex)
            return False
        
    async def get_user(self, user_id: str):
        if self.read != 'True':
            return 'Чтение данных запрещено'
        user = await UserRepositoryRedis.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Пользователь не найден',
            )
        try:
            return UserRespRedis(
                id = user['id'],
                surname = user['surname'],
                name = user['name'],
                patronymic = user['patronymic'],
            )
        except Exception as some_ex:
            print(some_ex)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    async def create_user(
        self,
        surname: str,
        name: str,
        patronymic: str,
    ):
        if self.create != 'True':
            return 'Добавление данных запрещено'
        try:
            user_id = str(uuid.uuid4())
            pipeline = await UserRepositoryRedis.REDIS_INSTANCE.pipeline(transaction=True)
            await pipeline.hmset(
                user_id,
                {   'id': user_id,
                    'surname': surname,
                    'name': name,
                    'patronymic': patronymic,
                }
            )
            await pipeline.execute()
            user = await UserRepositoryRedis.REDIS_INSTANCE.hgetall(user_id)
            return UserRespRedis(
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
            )

    async def update_user(
        self,
        surname: str,
        name: str,
        patronymic: str,
        user_id: str,
    ):
        if self.update != 'True':
            return 'Обновление данных запрещено'
        user = await UserRepositoryRedis.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Пользователь не найден',
            )
        try:
            pipeline = await UserRepositoryRedis.REDIS_INSTANCE.pipeline(transaction=True)
            await pipeline.hmset(
                user_id,
                {   'id': user_id,
                    'surname': surname,
                    'name': name,
                    'patronymic': patronymic,
                }
            )
            await pipeline.execute()
            user = await UserRepositoryRedis.REDIS_INSTANCE.hgetall(user_id)
            return UserUpdateRespRedis(
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
            )

    async def delete_user(self, user_id: str):
        if self.delete != 'True':
            return 'Удаление данных запрещено'
        user = await UserRepositoryRedis.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Пользователь не найден',
            )
        try:
            pipeline = await UserRepositoryRedis.REDIS_INSTANCE.pipeline(transaction=True)
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
            )
 



if settings.no_sql == 'True':
    print('no sql')
    user_repository = UserRepositoryRedis(
        settings.create,
        settings.update,
        settings.read,
        settings.delete,
    )
else:
    print('sql')
    user_repository = UserRepositoryPostgre(
        settings.create,
        settings.update,
        settings.read,
        settings.delete,
    )
