from sqlalchemy.ext.asyncio import create_async_engine

from fastapi.security import OAuth2

oauth2_scheme = OAuth2()


class EncryptConfig(object):
    """
    配置加密密钥
    key应为8-24位
    """
    password_key: str = '!@#$%^~~!qwg'
    token_key: str = '!@#$%^~~&'
    SECRET_KEY = "09d25e094f5wes52556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 10080


class BaseConfig(object):
    """
    数据库配置
    """
    # HOST = "49.232.14.115"
    HOST = "127.0.0.1"
    USER = 'www'
    PASSWORD = '-xFn9y2mK,dgfVVQ5#'
    PORT = '3306'
    DATABASE = 'myTestBase'

    DATABASE_URL = f"mysql+aiomysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}?charset=utf8"


async_engine = create_async_engine(BaseConfig.DATABASE_URL, echo=False, future=True)
# engine = create_engine(BaseConfig.DATABASE_URL, echo=True, future=True)

REDIS_CONFIG = {
    # "address": "redis://49.232.14.115:6379",
    "address": "redis://127.0.0.1:6379",
    # "password": "",
    "encoding": "utf-8",
    "timeout": 1,
}


class AppConfig(object):
    config = {
        'app': 'main:app',
        'host': '0.0.0.0',
        'port': 5001,
        'debug': False,
        'reload': True,
        'workers': 8,
    }
