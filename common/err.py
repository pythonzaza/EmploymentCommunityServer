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
        THROTTLE_ERR = 10006  # 访问频率过高
        INDEX_ERR = 10007  # 索引越界异常

    class User(IntEnum):
        USER_REPEAT = 20001  # 用户已存在
        ACCOUNT_OR_PWD_ERR = 20002  # 账号或密码错误
        ACCOUNT_DISABLE = 20003  # 账号被禁用
        USER_NOT_EXIST = 20004  # 用户已存在

    class Article(IntEnum):
        TYPE_NOT_EXIST = 30001  # 分类不存在

    class EnterPrise(IntEnum):
        ENTERPRISE_EXIST = 40001  # 企业已存在
        ENTERPRISE_NOT_EXIST = 40002  # 企业不存在

    class MessageBoard(IntEnum):
        MESSAGE_NOT_EXIST = 50001  # 留言不存在
        PERMISSIONS_ERR = 50002  # 权限异常
        STATUS_ERR = 50003  # 权限异常
