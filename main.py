from fastapi import FastAPI, Request, Depends
from fastapi.responses import JSONResponse
from fastapi.exception_handlers import request_validation_exception_handler
from fastapi.exceptions import RequestValidationError
from fastapi.security import HTTPBearer
from fastapi.middleware.cors import CORSMiddleware

from controller.common_controller import common_router
from controller.article_controller import article_router
from controller.enterprise_controller import enterprise_router
from controller.message_board_controller import message_board_router

from schema_models.base_model import RespModel422
from common.err import HTTPException, ErrEnum

from middleware.init_middleware import InitMiddleware
from middleware.throttle_middleware import ThrottleMiddleware
from middleware.exception_handler_middleware import ExceptionMiddleware

from configs import AppConfig

app = FastAPI(title='EmploymentCommunity')

# swagger身份验证器
OAuth2 = HTTPBearer()

# 跨域支持
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(ThrottleMiddleware)
app.add_middleware(InitMiddleware)
app.add_middleware(ExceptionMiddleware)


# @app.middleware('http')
# async def get_db(request: Request, call_next, ):
#     res = await call_next(request)
#     return res


# 注入全局异常类
@app.exception_handler(HTTPException)
async def unicorn_exception_handler(request: Request, err: HTTPException):
    """
    注入全局异常类
    :param request:
    :param err:
    :return:
    """
    return JSONResponse(
        content={
            "message": err.message,
            "status": err.status,
            "data": str(err.data) if AppConfig['debug'] else "",
        },
    )


# 修改格式校验异常的响应格式
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    # print(f"OMG! The client sent invalid data!: {exc}")

    error = exc.errors()[0]
    message = f'{".".join(error.get("loc"))} : {error.get("msg")};'

    return JSONResponse(
        content={
            "message": '数据格式异常',
            "status": ErrEnum.Common.PARAMS_ERR,
            "data": message,
        },
    )


# 路由配置
app.include_router(common_router, prefix='/common', tags=["公共"], responses={422: {"model": RespModel422}})
# app.include_router(article_router, prefix='/article', tags=["Article"])
app.include_router(enterprise_router, prefix='/enterprise', tags=["企业"], responses={422: {"model": RespModel422}})
app.include_router(message_board_router, prefix='/messageBoard', tags=["留言板"], responses={422: {"model": RespModel422}})

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(**AppConfig)
