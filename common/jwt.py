from fastapi import Depends, Request, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from aioredis import Redis
from datetime import datetime, timezone, timedelta

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


async def get_platform(platform: str = Header("web", description="平台")) -> str:
    """
    从headers获取平台参数
    :param platform: 平台
    :return: str 平台
    """
    if platform := platform.lower() not in ["web", "android", "ios"]:
        HTTPException(status=ErrEnum.Common.TOKEN_ERR, message="不支持的platform")
    return platform


async def jwt_auth(request: Request, platform: str = Depends(get_platform),
                   token: HTTPAuthorizationCredentials = Depends(http_bearer)) -> int:
    """
    JWT认证
    解析jwt, 并将用户信息挂载到request.state上
    :param request: 请求对象
    :param platform: 平台
    :param token: token
    :return: 用户id
    """

    http_exception = HTTPException(status=ErrEnum.Common.TOKEN_ERR, message="Token 验证失败")

    if token is None:
        http_exception.message = "无效Token"
        raise http_exception

    # 解析token
    token_data: TokenData = await Encrypt.parse_token(token.credentials)

    # 检查服务端Token
    redis: Redis = request.state.redis
    token_key = await get_token_key(token_data.user_id, platform)
    _token = await redis.get(token_key)

    if not _token:
        http_exception.message = "Token失效"
        raise http_exception

    # noinspection PyPep8Naming
    BeiJing: timezone = timezone(timedelta(hours=8))
    if token_data.exp < datetime.utcnow().astimezone(BeiJing):
        # token静默续期
        key_ttl = await redis.ttl(token_key)
        if key_ttl < EncryptConfig.ACCESS_TOKEN_EXPIRE_SECONDS:
            await redis.set(name=token_key, value=1, ex=EncryptConfig.ACCESS_TOKEN_EXPIRE_SECONDS)

    request.scope["user"] = token_data.user_id
    request.scope["auth"] = token_data
    return token_data.user_id
