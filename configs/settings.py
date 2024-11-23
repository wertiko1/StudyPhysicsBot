class CacheSettings:
    redis_url: str = "redis://redis:6379/0"
    state_ttl: int | None = None
    data_ttl: int | None = None
