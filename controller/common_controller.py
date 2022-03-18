from fastapi import APIRouter, Request

from schema_models.user_models import (
    UserRegisterIn, UserInfoOut, UserInfoOutData, UserLoginIn
)
from servers.user_servers import User

common_router = APIRouter()


@common_router.get("/test")
async def test(string: str):
    return string


@common_router.post("/register", name="注册", response_model=UserInfoOut)
async def register(request: Request, new_user: UserRegisterIn):
    """
    ## 注册
    新用户注册时调用, 邀请码和验证码暂未启用
    """
    user = User(request)
    new_user = await user.register(new_user)
    token = await user.create_token(new_user)

    data = UserInfoOutData.from_orm(new_user)
    data.token = token

    return UserInfoOut(data=data)


@common_router.post("/login", name="登录")
async def login(request: Request, login_user: UserLoginIn):
    """
    ## 登录
    """
    user = User(request)
    login_user = await user.login(login_user)
    data = UserInfoOutData.from_orm(login_user)
    return UserInfoOut(data=data)
