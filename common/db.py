from aioredis import Redis, from_url
from sqlalchemy.ext.asyncio import AsyncSession
from collections.abc import AsyncGenerator
from sqlalchemy.orm import sessionmaker, registry

from configs import async_engine, RedisConfig

mapper_registry = registry()
Base = mapper_registry.generate_base()


async_db_session = sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)


async def get_async_db() -> AsyncSession:
    async with async_db_session() as db_session:
        return db_session

# async def get_async_db() -> AsyncGenerator:
#     async with async_db_session() as db_session:
#         yield db_session


async def get_async_redis_session() -> Redis:
    redis_pool = await from_url(RedisConfig.HOST, encoding=RedisConfig.ENCODING, )
    async with redis_pool.client() as redis_session:
        return redis_session


__all__ = [Base, async_db_session, get_async_redis_session, get_async_db]
