from fastapi import FastAPI, Request, Depends
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
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

app = FastAPI(title='EmploymentCommunity', responses={422: {"model": RespModel422}})

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
            "status": ErrEnum.NETWORK.PARAMS_VALIDATION_ERR,
            "data": message,
        },
    )


# 路由配置
app.include_router(common_router, prefix='/common', tags=["公共"])
# app.include_router(article_router, prefix='/article', tags=["Article"])
app.include_router(enterprise_router, prefix='/enterprise', tags=["企业"] )
app.include_router(message_board_router, prefix='/messageBoard', tags=["留言板"])

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(**AppConfig)
