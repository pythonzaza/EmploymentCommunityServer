from schema_models.user_models import UserRegisterIn
from aioredis import Redis
from sqlalchemy.ext.asyncio import AsyncSession


class User(object):
    def __init__(self, db: AsyncSession, redis: Redis):
        self.db = db
        self.redis = redis

    @staticmethod
    async def get_user_by_user_name(user: UserRegisterIn):
        pass
