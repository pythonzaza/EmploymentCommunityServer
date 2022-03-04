from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware, DispatchFunction, RequestResponseEndpoint
from starlette.responses import Response
from starlette.types import ASGIApp
from aioredis import Redis

from common.err import ErrEnum
from common.logger import logger


class ThrottleMiddleware(BaseHTTPMiddleware):
    """
    获取数据库连接中间件
    """

    def __init__(self, app: ASGIApp, dispatch: DispatchFunction = None) -> None:
        super().__init__(app, dispatch)

    @staticmethod
    async def get_hash_path(hash_path):
        return f"throttle:{hash_path}"

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        hash_path = request.client.host + request.method + request.headers
        key = await self.get_hash_path(hash_path)
        redis: Redis = request.state.redis
        if await redis.get(key):
            return JSONResponse(content={})
        await redis.set(key, True, ex=1)
        response = await call_next(request)
        return response
