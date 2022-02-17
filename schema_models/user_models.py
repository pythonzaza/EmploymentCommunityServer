from pydantic import BaseModel, Field, EmailStr


class UserRegisterIn(BaseModel):
    user_name: str = Field(..., description="用户名", min_length=6, max_length=20)
    password: str = Field(..., description="密码", min_length=8, max_length=20, )
    email: EmailStr
