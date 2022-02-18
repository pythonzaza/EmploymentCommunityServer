from typing import Any
from fastapi.exceptions import RequestValidationError
from enum import IntEnum


class HTTPException(Exception):

    def __init__(self, message: str, status: int, data=''):
        self.message: str = message
        self.status: int = status
        self.data: Any = data


class ValidationException(RequestValidationError):

    def __init__(self, errors, *, message: str, status: int, data: Any, body: Any = None) -> None:
        self.message: str = message
        self.status: int = status
        self.data: Any = data
        super().__init__(errors, body=body)


class ErrEnum:
    class Common(IntEnum):
        NETWORK_ERR = 10000  # 网络繁忙
        DB_ERR = 10002  # 数据库异常
        REDIS_ERR = 10003  # Redis异常
        PARAMS_ERR = 10004  # 参数异常
        TOKEN_ERR = 10005  # token异常

    class User(IntEnum):
        USER_REPEAT = 20001  # 用户已存在
        ACCOUNT_OR_PWD_ERR = 20002  # 账号或密码错误
