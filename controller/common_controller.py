from fastapi import APIRouter, Request

from schema_models.user_models import UserRegisterIn, UserRegisterOut, _UserRegisterOut
from servers.user_servers import User

common_router = APIRouter()


@common_router.get("/test")
async def test(string: str):
    return string


@common_router.post("/register", name="注册", response_model=UserRegisterOut)
async def register(request: Request, new_user: UserRegisterIn):
    """
    ## 注册
    新用户注册时调用, 邀请码和验证码暂未启用
    """
    user = User(request)
    new_user = await user.register(new_user)
    await user.creat_token(new_user)

    return UserRegisterOut(data=_UserRegisterOut.from_orm(new_user))
