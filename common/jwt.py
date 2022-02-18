from fastapi import Request
from aioredis import Redis
from datetime import datetime

from configs import EncryptConfig
from common.encrypt import Encrypt
from common.err import HTTPException, ErrEnum
from schema_models.common_models import TokenData


async def get_token_key(user_id, platform):
    """
    获取token的keyName
    :parma user_id 用户id
    :parma platform 平台
    """
    return f"user:token:{platform}:userId{user_id}"


async def verify_token(request: Request) -> TokenData:
    """
    验证token->依赖项
    :parma request 请求对象
    """
    authorization: str = request.headers.get('Authorization', '')
    token_type, token = authorization.split()

    if token_type != 'Bearer':
        raise HTTPException(status=ErrEnum.Common.TOKEN_ERR, message="token异常")

    token_data = await Encrypt.parse_token(token)

    redis_db: Redis = request.state.redis
    token_key = await get_token_key(token_data.user_id, token_data.platform)
    server_token = await redis_db.get(token_key)

    if not server_token:
        raise HTTPException(status=ErrEnum.Common.TOKEN_ERR, message="Token异常")

    if token_data.exp < datetime.now():
        key_ttl = await redis_db.ttl(token_key)
        if key_ttl < EncryptConfig.ACCESS_TOKEN_EXPIRE_SECONDS:
            await redis_db.set(name=token_key, value=token, ex=EncryptConfig.ACCESS_TOKEN_EXPIRE_SECONDS)

    # request.scope['user'] = token_data.user_id
    # request.scope['auth'] = token_data
    return token_data
