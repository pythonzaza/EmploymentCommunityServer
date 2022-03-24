import asyncio
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware, DispatchFunction, RequestResponseEndpoint
from starlette.responses import Response
from starlette.types import ASGIApp

from common.db import get_async_redis_session, get_async_db
from common.err import ErrEnum, HTTPException
from common.logger import logger


class InitMiddleware(BaseHTTPMiddleware):
    """
    获取数据库连接中间件
    """

    def __init__(self, app: ASGIApp, dispatch: DispatchFunction = None) -> None:
        super().__init__(app, dispatch)

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        try:
            request.state.db = await get_async_db()
            request.state.redis = await get_async_redis_session()
            response = await call_next(request)
            await request.state.redis.close()
            return response

        except HTTPException as err:
            raise err
        except Exception as err:
            logger.error(str(err))
            return JSONResponse(content={"status": ErrEnum.Common.NETWORK_ERR, "message": "系统异常", "data": str(err)})
