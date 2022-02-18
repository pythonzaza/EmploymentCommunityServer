from fastapi import Request
from aioredis import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, or_
from datetime import datetime

from configs import EncryptConfig
from common.err import HTTPException, ErrEnum
from common.encrypt import Encrypt
from common.jwt import get_token_key
from common.logger import logger
from schema_models.user_models import UserRegisterIn
from schema_models.common_models import TokenData
from models.user_models import UserModel


class User(object):
    def __init__(self, request: Request, ):
        self.request = request
        self.db: AsyncSession = request.state.db
        self.redis: Redis = request.state.redis

    async def get_user_by_user_name(self, user: UserRegisterIn):
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

    @staticmethod
    def get_token_key(user_id, platform):
        return f"user:token:{platform}:userId{user_id}"

    async def creat_token(self, user: UserModel, platform: str = "web"):
        token_data = {
            "user_id": user.id,
            "account": user.account,
            # "token": user.token,
            "platform": platform,
        }
        token_data = TokenData(**token_data)
        token = await Encrypt.create_token(token_data)
        token_key = await get_token_key(user.id, platform)
        result = await self.redis.set(token_key, token, ex=EncryptConfig.ACCESS_TOKEN_EXPIRE_SECONDS * 2)
        if result:
            user.token = token
            return
        else:
            raise HTTPException(message='Redis写入失败', status=ErrEnum.Common.REDIS_ERR)
