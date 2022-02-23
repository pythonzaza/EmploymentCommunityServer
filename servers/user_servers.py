from fastapi import Request
from aioredis import Redis
from sqlalchemy.future import Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine.result import Result, ChunkedIteratorResult
from sqlalchemy import select, insert, or_, and_
from datetime import datetime

from configs import EncryptConfig
from common.err import HTTPException, ErrEnum
from common.encrypt import Encrypt
from common.jwt import get_token_key
from common.logger import logger
from schema_models.user_models import UserRegisterIn, UserLoginIn
from schema_models.common_models import TokenData
from models.user_models import UserModel


class User(object):
    def __init__(self, request: Request, ):
        self.request = request
        self.db: AsyncSession = request.state.db
        self.redis: Redis = request.state.redis

    async def get_user_by_user_name(self, user: UserRegisterIn) -> UserModel.id:
        stmt = select([UserModel.id]).where(or_(UserModel.account == user.account, UserModel.email == user.email))

        result = await self.db.execute(stmt)
        user = result.scalars().first()
        return user

    async def register(self, user: UserRegisterIn) -> UserModel:

        async with self.db.begin():
            old_user = await self.get_user_by_user_name(user)
            if old_user:
                raise HTTPException(status=ErrEnum.User.USER_REPEAT, message="账户已存在", data="账户已存在")

            try:
                user.password = await Encrypt.encrypt_password(user.password)
                new_user = user.dict()
                root_token = await Encrypt.encrypt_password(f'{user.account}-{user.email}')
                new_user.update({
                    "register_ip": self.request.client.host,
                    "register_time": datetime.now(),
                    "token": root_token
                })

                stmt = insert(UserModel).values(**new_user)

                result = await self.db.execute(stmt)
                if result.is_insert:
                    await self.db.commit()
                    new_user["id"] = result.inserted_primary_key[0]
                    new_user = UserModel(**new_user)
                else:
                    logger.error(f"数据写入失败->{stmt}")
                    raise Exception("数据写入失败")
                return new_user

            except Exception as err:
                logger.error(err)
                raise HTTPException(status=ErrEnum.Common.NETWORK_ERR, message="系统异常", data=err)

    async def create_token(self, user: UserModel, platform: str = "web") -> str:
        token_data = {
            "user_id": user.id,
            "account": user.account,
            "ip": self.request.client.host,
            "platform": platform,
        }
        token_data = TokenData(**token_data)
        token = await Encrypt.create_token(token_data, token=user.token)
        token_key = await get_token_key(user.id, platform)
        result = await self.redis.set(token_key, token, ex=EncryptConfig.ACCESS_TOKEN_EXPIRE_SECONDS * 2)
        if result:
            # user.token = token
            return token
        else:
            raise HTTPException(message='Redis写入失败', status=ErrEnum.Common.REDIS_ERR)

    async def _find_user(self, user: UserLoginIn) -> UserModel:

        stmt: Select = select(UserModel).where(
            or_(UserModel.account == user.account, UserModel.email == user.email),
            UserModel.password == user.password)
        result: ChunkedIteratorResult = await self.db.execute(stmt)
        user = result.scalars().first()

        if not user:
            raise HTTPException(status=ErrEnum.User.ACCOUNT_OR_PWD_ERR, message="账号或密码错误")
        return user

    async def login(self, login_user: UserLoginIn):
        login_user.password = await Encrypt.encrypt_password(login_user.password)
        async with self.db.begin():
            if user := await self._find_user(login_user):
                new_token = await self.create_token(user=user)
        user.token = new_token
        return user
