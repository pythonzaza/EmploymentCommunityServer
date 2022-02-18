from typing import Union
from pydantic import BaseModel, Field, EmailStr

from schema_models.base_model import RespModel


class UserRegisterIn(BaseModel):
    name: str = Field(..., description="用户名", min_length=6, max_length=20)
    account: str = Field(..., description="登录账号", min_length=6, max_length=20)
    password: str = Field(..., description="密码", min_length=8, max_length=20)
    email: EmailStr = Field(..., description="邮箱")
    code: str = Field('', description="验证码-暂未启用", max_length=6)
    invite_code: str = Field('', description="邀请码-暂未启用", max_length=6)

    def dict(self, *, include: Union['AbstractSetIntStr', 'MappingIntStrAny'] = None,
             exclude: Union['AbstractSetIntStr', 'MappingIntStrAny'] = None, by_alias: bool = False,
             skip_defaults: bool = None, exclude_unset: bool = False, exclude_defaults: bool = False,
             exclude_none: bool = False) -> 'DictStrAny':
        exclude = self.Config.exclude if exclude is None else None
        return super().dict(include=include, exclude=exclude, by_alias=by_alias, skip_defaults=skip_defaults,
                            exclude_unset=exclude_unset, exclude_defaults=exclude_defaults, exclude_none=exclude_none)

    class Config:
        exclude = {"code", "invite_code"}


class _UserRegisterOut(BaseModel):
    name: str = Field(..., description="用户名", )
    account: str = Field(..., description="登录账号", )
    token: str = Field(..., description="token")

    class Config:
        orm_mode = True


class UserRegisterOut(RespModel):
    data: _UserRegisterOut
