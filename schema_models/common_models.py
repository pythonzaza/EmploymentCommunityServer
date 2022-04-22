from pydantic import BaseModel, Field
from datetime import datetime


class TokenData(BaseModel):
    user_id: int = Field(..., description="用户id")
    account: str = Field(..., description="用户账号")
    # token: str = Field(..., description="根token")
    platform: str = Field(..., description="登录平台")
    ip: str = Field(..., description="登录ip")
    exp: datetime = Field(0, description="初始过期时间")


class IpDetailsModel(BaseModel):
    """
    city:str,
    coordinates:str,
    """
    ip: str = Field(..., description="ip地址")
    city: str = Field("", description="国家-省/市-区/县")
    coordinates: str = Field("", description="坐标-经度,纬度")
