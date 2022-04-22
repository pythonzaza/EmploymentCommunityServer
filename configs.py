from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.pool import AsyncAdaptedQueuePool
from pydantic import BaseSettings, Field


class BaseSetting(BaseSettings):
    class Config:
        env_file = '.env'


class EncryptConfig(BaseSetting):
    """
    配置加密密钥
    key应为8-24位
    """
    PASSWORD_KEY: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_SECONDS: int = 10080 * 60  # 七天

    class Config:
        env_prefix = "ENCRYPT_"


class BaseConfig(BaseSetting):
    """
    数据库配置
    """
    HOST: str
    USER: str
    PASSWORD: str
    PORT: int
    DATABASE: str
    DATABASE_URL: str
    CHARSET: str = "UTF8MB4"

    ECHO = False
    ECHO_POOL: bool = False
    MAX_OVERFLOW: int = 20

    class Config:
        env_prefix = "DATABASE_"


class RedisConfig(BaseSetting):
    # "address": "redis://49.232.14.115:6379",
    HOST: str = "redis://127.0.0.1:6379"
    # "password": "",
    ENCODING: str = "utf-8"
    TIMEOUT: int = 1

    class Config:
        env_prefix = "REDIS_"


class AppConfig(BaseSetting):
    app: str = Field('main:app', env="APP"),
    host: str = Field('0.0.0.0', env="HOST"),
    port: int = Field(5001, env="PORT"),
    debug: bool = Field(False, env="DEBUG"),
    reload: bool = Field(True, env="RELOAD"),
    workers: int = Field(8, env="WORKERS"),

    class Config:
        env_prefix = "APP_"


class CommonConfigs(BaseSetting):
    """
    通用配置
    """

    # QUERY_IP_URL: str = "http://ip-api.com/batch?lang=zh-CN&fields=778461"
    # QUERY_IP_URL: str = "http://ip-api.com/json/{}?lang=zh-CN&fields=13357277"

    class Config:
        env_prefix = "COMMON_"


EncryptConfig = EncryptConfig()
BaseConfig = BaseConfig()
RedisConfig = RedisConfig()
AppConfig = AppConfig()
CommonConfigs = CommonConfigs()

if not BaseConfig.DATABASE_URL:
    BaseConfig.DATABASE_URL = f"mysql+aiomysql://{BaseConfig.USER}:{BaseConfig.PASSWORD}@" \
                              f"{BaseConfig.HOST}:{BaseConfig.PORT}/{BaseConfig.DATABASE}?charset={BaseConfig.CHARSET}"

async_engine = create_async_engine(BaseConfig.DATABASE_URL, echo=BaseConfig.ECHO, future=True,
                                   echo_pool=BaseConfig.ECHO_POOL, max_overflow=BaseConfig.MAX_OVERFLOW,
                                   poolclass=AsyncAdaptedQueuePool)

__all__ = ["EncryptConfig", "RedisConfig", "AppConfig", "async_engine", "CommonConfigs"]
