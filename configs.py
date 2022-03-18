from sqlalchemy.ext.asyncio import create_async_engine

from fastapi.security import OAuth2

oauth2_scheme = OAuth2()


class EncryptConfig(object):
    """
    配置加密密钥
    key应为8-24位
    """
    PASSWORD_KEY: str = '!@#$%^~~!qwg'
    SECRET_KEY = "96974c25dec188a196904287f4db7353e8bd9806b907a3eda59d71eddae3e053"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_SECONDS = 10080 * 60  # 七天


class BaseConfig(object):
    """
    数据库配置
    """
    HOST = "127.0.0.1"
    USER = 'root'
    PASSWORD = '123456'
    PORT = '3306'
    DATABASE = 'EmploymentCommunity'

    DATABASE_URL = f"mysql+aiomysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}?charset=UTF8MB4"


async_engine = create_async_engine(BaseConfig.DATABASE_URL, echo=True, future=True)


class RedisConfig:
    # "address": "redis://49.232.14.115:6379",
    host = "redis://127.0.0.1:6379"
    # "password": "",
    encoding = "utf-8"
    timeout = 1


class AppConfig(object):
    config = {
        'app': 'main:app',
        'host': '0.0.0.0',
        'port': 5001,
        'debug': False,
        'reload': True,
        'workers': 8,
    }
