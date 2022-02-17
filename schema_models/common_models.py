from pydantic import BaseModel, Field


class TokenData(BaseModel):
    user_id: int = Field(..., description="用户id")
    token: str = Field(..., description="根token")
    platform: str = Field(..., description="登录平台")
    exp: int = Field(0, description="初始过期时间")
