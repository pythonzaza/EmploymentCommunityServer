import asyncio
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware, DispatchFunction, RequestResponseEndpoint
from starlette.responses import Response
from starlette.types import ASGIApp

from common.db import get_async_redis_session, get_async_db


class InitMiddleware(BaseHTTPMiddleware):
    """
    获取数据库连接中间件
    """

    def __init__(self, app: ASGIApp, dispatch: DispatchFunction = None) -> None:
        super().__init__(app, dispatch)

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        # tasks = [get_async_db(), get_async_redis_session()]

        response = {"message": "系统异常", "status": 10000}
        try:
            # noinspection PyTupleAssignmentBalance
            request.state.db = await get_async_db()
            request.state.redis = await get_async_redis_session()
            response = await call_next(request)
            await request.state.db.close()
            await request.state.redis.close()
            return response
        except Exception as err:
            print(err)
            return response
