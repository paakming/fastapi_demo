import redis.asyncio as redis
from redis.asyncio import Redis

from app.core.config import settings

# Redis连接池
redis_pool = redis.ConnectionPool(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    password=settings.REDIS_PASSWORD or None,
    decode_responses=True,
    max_connections=20,
)

# Redis客户端
redis_client = redis.Redis(connection_pool=redis_pool)


async def get_redis() -> Redis:
    """
    获取Redis连接的依赖项
    """
    return redis_client


async def close_redis():
    """
    关闭Redis连接
    """
    await redis_client.close()
