from .dbs.database import DataBase
from .dbs.cache import RedisClient
from src.settings.base import CacheSettings


class SetupData:
    def __init__(self) -> None:
        self._db_client = DataBase()
        self._redis_client = RedisClient(
            redis_url=CacheSettings.REDIS_URL,
            state_ttl=CacheSettings.STATE_TTL,
            data_ttl=CacheSettings.DATA_TTL
        )

    def get_redis_client(self) -> RedisClient:
        return self._redis_client

    def get_db_client(self) -> DataBase:
        return self._db_client
