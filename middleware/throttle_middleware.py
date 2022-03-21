import json
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware, DispatchFunction, RequestResponseEndpoint
from starlette.responses import Response
from starlette.types import ASGIApp
from aioredis import Redis

from common.err import ErrEnum
from common.encrypt import Encrypt
from schema_models.base_model import RespModel
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
        # body = {}
        # try:
        #     body = await request.json()
        # except Exception as e:
        #     print(e)

        hash_path = f'{request.url.netloc}{request.url.path}:{request.method}:' + \
                    f'{request.headers.get("Authorization", "")}:{request.client.host}'

        hash_path = await Encrypt.md5(hash_path)

        key = await self.get_hash_path(hash_path)
        redis: Redis = request.state.redis
        old = await redis.get(key)
        if old:
            resp = RespModel(status=ErrEnum.Common.THROTTLE_ERR, message="访问频率过高,请稍后重试")
            return JSONResponse(content=resp.json(ensure_ascii=False))
        await redis.set(key, 1, ex=1)

        response = await call_next(request)
        return response
