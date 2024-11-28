from redis.asyncio import Redis


class RedisClient:
    def __init__(self, redis_url: str, state_ttl: int, data_ttl: int) -> None:
        self._client = Redis.from_url(redis_url)
        self.state_ttl = state_ttl
        self.data_ttl = data_ttl

    async def ping(self) -> None:
        return await self._client.ping()

    def get_client(self) -> Redis:
        return self._client
