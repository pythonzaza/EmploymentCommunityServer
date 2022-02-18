from pydantic import BaseModel, Field, EmailStr


class UserRegisterIn(BaseModel):
    name: str = Field(..., description="用户名", min_length=6, max_length=20)
    account: str = Field(..., description="登录账号", min_length=6, max_length=20)
    password: str = Field(..., description="密码", min_length=8, max_length=20)
    email: EmailStr = Field(..., description="邮箱")
    code: str = Field('', description="验证码-暂未启用", max_length=6)
    invite_code: str = Field('', description="邀请码-暂未启用", max_length=6)
