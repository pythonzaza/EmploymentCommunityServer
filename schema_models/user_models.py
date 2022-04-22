from pydantic import BaseModel, Field, EmailStr, root_validator
from typing import Optional, Any, List
from datetime import datetime

from schema_models.base_model import RespModel


class UserBase(BaseModel):
    """
    Base class for User model
    """
    account: str = Field(..., description="登录账号", min_length=6, max_length=20)
    password: str = Field(..., description="密码", min_length=8, max_length=20)
    email: EmailStr = Field(..., description="邮箱")


class UserRegisterIn(UserBase):
    """
    用户注册输入模型
    """
    name: str = Field(..., description="用户名", min_length=6, max_length=20)
    code: str = Field('', description="验证码-暂未启用", max_length=6)
    invite_code: str = Field('', description="邀请码-暂未启用", max_length=6)

    def dict(self, *, include=None, exclude=None, by_alias: bool = False, skip_defaults: bool = None,
             exclude_unset: bool = False, exclude_defaults: bool = False, exclude_none: bool = False):
        exclude = self.Config.exclude if exclude is None else None
        return super().dict(include=include, exclude=exclude, by_alias=by_alias, skip_defaults=skip_defaults,
                            exclude_unset=exclude_unset, exclude_defaults=exclude_defaults, exclude_none=exclude_none)

    class Config:
        exclude = {"code", "invite_code"}


class UserInfoOutData(BaseModel):
    """
    内部用户信息输出模型
    """
    name: str = Field(..., description="用户名", )
    account: str = Field(..., description="登录账号", )
    token: str = Field(..., description="token")

    class Config:
        orm_mode = True


class UserInfoOut(RespModel):
    """
    用户信息输出模型
    """
    data: UserInfoOutData


class UserLoginIn(UserBase):
    """
    用户登录输入模型
    """
    account: Optional[str] = Field(None, description="登录账号", min_length=6, max_length=20)
    password: str = Field(..., description="密码", min_length=8, max_length=20)
    email: Optional[EmailStr] = Field(None, description="邮箱")

    @root_validator
    def check_account(cls, values):
        account, email = values.get('account'), values.get('email')
        if not account and not email:
            raise ValueError('account和email需至少有一项填写', )

        if account and email:
            raise ValueError('account和email只能填写其中一项', )

        return values


class UserLoginLog(BaseModel):
    """
    用户登录日志输出模型
    """
    # user_id: int = Field(..., description="用户id")
    login_ip: str = Field(..., description="登录ip")
    city: str = Field(..., description="登录城市")
    coordinates: str = Field(..., description="登录城市坐标")
    is_login: str = Field(..., description="是否登录成功")
    remark: str = Field(..., description="备注")
    # verify: str = Field(..., description="校验字段")
    create_time: datetime = Field(..., description="登录时间")


class UserLoginLogListOut(RespModel):
    """
    用户登录日志列表输出模型
    """
    data: List[UserLoginLog]
