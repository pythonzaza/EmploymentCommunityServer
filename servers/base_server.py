from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession
from aioredis import Redis


class BaseServer(object):
    def __init__(self, request: Request, ):
        self.request = request
        self.db: AsyncSession = request.state.db
        self.redis: Redis = request.state.redis
