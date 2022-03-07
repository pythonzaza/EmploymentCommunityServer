from fastapi import FastAPI, Request, Depends
from fastapi.responses import JSONResponse
from fastapi.exception_handlers import request_validation_exception_handler
from fastapi.exceptions import RequestValidationError
from fastapi.security import HTTPBearer
from fastapi.middleware.cors import CORSMiddleware

from controller.common_controller import common_router
from common.err import HTTPException, ErrEnum
from middleware.init_middleware import InitMiddleware
from middleware.throttle_middleware import ThrottleMiddleware

from configs import AppConfig

app = FastAPI(title='EmploymentCommunity-就业社区')

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
            "data": str(err.data) if AppConfig.config['debug'] else [],
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
app.include_router(common_router, prefix='/common', tags=["Common"])

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(**AppConfig.config)
