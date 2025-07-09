from redis.asyncio import ConnectionPool, Redis


def create_redis(url: str) -> Redis:
    return Redis(connection_pool=ConnectionPool.from_url(url=url))  # type: ignore
