from time import time
from random import randint
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware, DispatchFunction, RequestResponseEndpoint
from starlette.responses import Response
from starlette.types import ASGIApp

from common.db import get_async_redis_session, get_async_db
from common.logger import logger

class InitMiddleware(BaseHTTPMiddleware):
    """
    获取数据库连接中间件
    """

    def __init__(self, app: ASGIApp, dispatch: DispatchFunction = None) -> None:
        super().__init__(app, dispatch)

    @staticmethod
    async def create_request_id():
        _t = int((time() - 1649000000) * 10 ** 9)
        t = hex(_t)[2:]
        key = randint(100, 999)
        return f"{t}-{key}"

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        request.state.request_id = await self.create_request_id()
        logger.info(f"request_id: {request.state.request_id}{request.url.path}")

        request.state.db = await get_async_db()
        # request.state.db = await get_async_db().asend(None)
        request.state.redis = await get_async_redis_session()
        response = await call_next(request)
        await request.state.db.close()
        await request.state.redis.close()
        return response
