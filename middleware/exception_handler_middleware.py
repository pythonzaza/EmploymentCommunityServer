from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response
from sqlalchemy.exc import IntegrityError

from common.err import ErrEnum, HTTPException
from common.logger import logger
from configs import AppConfig


class ExceptionMiddleware(BaseHTTPMiddleware):
    """
    获取数据库连接中间件
    """

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        try:

            response = await call_next(request)

            return response

        except HTTPException as err:
            raise err

        except IntegrityError as err:
            logger.error(f"request_id:{request.state.request_id}=>{err}")
            return JSONResponse(
                content={
                    "status": ErrEnum.Common.INTEGRITY_ERR,
                    "message": "新数据已存在",
                    "data": str(err) if AppConfig.debug else ""
                }
            )

        except Exception as err:
            logger.error(f"request_id:{request.state.request_id}=>{err}")
            return JSONResponse(
                content={
                    "status": ErrEnum.NETWORK.NETWORK_ERR,
                    "message": "系统异常",
                    "data": str(err) if AppConfig.debug else ""
                }
            )
