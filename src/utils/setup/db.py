from configs.settings import CacheSettings
from .dbs.cache import RedisClient
from .dbs.database import DataBase


class SetupData:
    def __init__(self) -> None:
        self._db_client = DataBase()
        self._redis_client = RedisClient(
            redis_url=CacheSettings.redis_url,
            state_ttl=CacheSettings.state_ttl,
            data_ttl=CacheSettings.data_ttl
        )

    def get_redis_client(self) -> RedisClient:
        return self._redis_client

    def get_db_client(self) -> DataBase:
        return self._db_client
