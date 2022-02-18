from pydantic import BaseModel, Field
from datetime import datetime


class TokenData(BaseModel):
    user_id: int = Field(..., description="用户id")
    account: str = Field(..., description="用户账号")
    # token: str = Field(..., description="根token")
    platform: str = Field(..., description="登录平台")
    exp: datetime = Field(0, description="初始过期时间")
