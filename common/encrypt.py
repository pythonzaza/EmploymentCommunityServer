import hashlib
from jose import JWTError, jwt
from datetime import datetime, timedelta

from configs import EncryptConfig
from common.err import HTTPException, ErrEnum
from schema_models.common_models import TokenData


class Encrypt(object):

    @staticmethod
    async def encrypt_password(password: str) -> str:
        """
        获取加密后的密码
        :param password: 原始密码
        :return: str 加密后的密码
        """
        sha256 = hashlib.sha256()
        sha256.update((password + EncryptConfig.PASSWORD_KEY).encode())
        return sha256.hexdigest()

    async def verify_password(self, password: str, hash_password: str) -> bool:
        """
        密码验证
        :param password: 原始密码
        :param hash_password: 加密后的密码
        :return: 验证通过 True or False
        """
        __hash_password = self.encrypt_password(password)
        if __hash_password == hash_password:
            return True
        else:
            return False

    @staticmethod
    async def create_token(token_data: TokenData,
                           *, expires_delta: int = EncryptConfig.ACCESS_TOKEN_EXPIRE_SECONDS,
                           token: str = "") -> str:
        """
        创建token
        :param token_data:待加密的数据
        :param expires_delta: token过期时间 默认取配置文件
        :param token: token盐值, 根据用户生成
        :return: str token
        """
        expire = datetime.utcnow() + timedelta(seconds=expires_delta)
        token_data.exp = expire
        to_encode = token_data.dict()

        encoded_jwt = jwt.encode(to_encode, EncryptConfig.SECRET_KEY + token, algorithm=EncryptConfig.ALGORITHM)
        return encoded_jwt

    @staticmethod
    async def parse_token(token: str) -> TokenData:
        """
        解析token
        :param token: 待解析的token-jwt格式
        :return: TokenData 解析后的数据
        """
        try:
            user = jwt.decode(token, EncryptConfig.SECRET_KEY, algorithms=[EncryptConfig.ALGORITHM])
            if not isinstance(user, dict):
                raise HTTPException(message="token_data格式异常", status=ErrEnum.Common.TOKEN_ERR)
            return TokenData(**user)
        except JWTError as err:
            raise HTTPException(message=f"token解码异常:{err}", status=ErrEnum.Common.TOKEN_ENCRYPT)

    @staticmethod
    async def md5(text: str):
        """
        MD5加密方法
        :param text: 原始字符串
        :return: str 加密后的字符串
        """
        md5 = hashlib.md5()
        md5.update(text.encode())
        return md5.hexdigest()
