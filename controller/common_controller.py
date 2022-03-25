from fastapi import APIRouter, Request, Depends
from schema_models.user_models import (
    UserRegisterIn, UserInfoOut, UserInfoOutData, UserLoginIn
)

from servers.user_servers import UserServer
from common.depends import get_platform

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
    user = UserServer(request)
    new_user = await user.register(new_user)
    token = await user.create_token(new_user)

    data = UserInfoOutData.from_orm(new_user)
    data.token = token

    return UserInfoOut(data=data)


@common_router.post("/login", response_model=UserInfoOut, name="登录")
async def login(request: Request, login_user: UserLoginIn, platform: str = Depends(get_platform)):
    """
    ## 登录
    """
    user = UserServer(request)
    login_user = await user.login(login_user, platform)
    # data = UserInfoOutData.from_orm(login_user)
    return UserInfoOut(data=login_user)
