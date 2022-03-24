from fastapi import Depends, Request, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from aioredis import Redis
from typing import Union
from datetime import datetime,timezone,timedelta

from configs import EncryptConfig
from common.err import HTTPException, ErrEnum
from common.encrypt import Encrypt
from schema_models.common_models import TokenData

http_bearer = HTTPBearer(auto_error=False)


async def get_token_key(user_id: int, platform: str) -> str:
    """
    获取token的keyName
    :parma user_id 用户id
    :parma platform 平台
    """
    return f"user:token:{platform}:{user_id}"


async def jwt_auth(request: Request, platform: str = Header("web", description="平台"),
                   token: HTTPAuthorizationCredentials = Depends(http_bearer)) -> Union[int, HTTPException]:
    http_exception = HTTPException(status=ErrEnum.Common.TOKEN_ERR, message="Token 验证失败")

    if token is None:
        http_exception.message = "无效Token"
        return http_exception

    if platform.lower() not in ["web", "android", "ios"]:
        http_exception.message = "无效Platform"
        return http_exception

    # 解析token
    token_data = await Encrypt.parse_token(token.credentials)

    # 检查服务端Token
    redis: Redis = request.state.redis
    token_key = await get_token_key(token_data.user_id, platform)
    _token = await redis.get(token_key)

    if not _token:
        http_exception.message = "Token失效"
        return http_exception

    if token_data.exp < datetime.utcnow().astimezone(timezone(timedelta(hours=8))):
        # token静默续期
        key_ttl = await redis.ttl(token_key)
        if key_ttl < EncryptConfig.ACCESS_TOKEN_EXPIRE_SECONDS:
            await redis.set(name=token_key, value=1, ex=EncryptConfig.ACCESS_TOKEN_EXPIRE_SECONDS)

    request.scope["user"] = token_data.user_id
    request.scope["auth"] = token_data
    return token_data.user_id
