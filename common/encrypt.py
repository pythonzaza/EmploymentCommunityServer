import hashlib
from jose import JWTError, jwt
from typing import Union
from datetime import datetime, timedelta

from configs import EncryptConfig
from common.err import HTTPException
from schema_models.common_models import TokenData


class Encrypt(object):

    @staticmethod
    async def encrypt_password(password: str):
        """
        获取加密后的密码
        :param password: 原始密码
        :return:
        """
        sha256 = hashlib.sha256()
        sha256.update((password + EncryptConfig.PASSWORD_KEY).encode())
        return sha256.hexdigest()

    async def verify_password(self, password: str, hash_password: str) -> bool:
        """
        密码验证
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
        """
        expire = datetime.utcnow() + timedelta(seconds=expires_delta)
        token_data.exp = expire
        to_encode = token_data.dict()

        encoded_jwt = jwt.encode(to_encode, EncryptConfig.SECRET_KEY + token, algorithm=EncryptConfig.ALGORITHM)
        return encoded_jwt

    @staticmethod
    async def parse_token(token: str) -> Union[TokenData, HTTPException]:
        try:
            user = jwt.decode(token, EncryptConfig.SECRET_KEY, algorithms=[EncryptConfig.ALGORITHM])
            if not isinstance(user, dict):
                return HTTPException(message="token_data格式异常", status=20000)
            return TokenData(**user)
        except JWTError as err:
            raise HTTPException(message=f"token解码异常:{err}", status=20001)

    @staticmethod
    async def md5(text: str):
        md5 = hashlib.md5()
        md5.update(text.encode())
        return md5.hexdigest()
