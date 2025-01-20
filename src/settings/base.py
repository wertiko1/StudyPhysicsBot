from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Tuple


class LoggingConfig(BaseSettings):
    LEVEL: str = "DEBUG"
    PATH: str = "logs/bot.log"


class DatabaseSettings(BaseSettings):
    DB_HOST: str = "postgres"
    DB_PORT: int = 5432
    DB_USER: str = "user"
    DB_PASSWORD: str = "password"
    DB_NAME: str = "models"
    DB_MODELS: Tuple[str] = ("src.models", "aerich.models")
    TEST_URL: str = "sqlite://db/app.db"

    @property
    def url(self):
        return f"asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


class CacheSettings(BaseSettings):
    REDIS_URL: str = "redis://redis:6379/0"
    STATE_TTL: int | None = None
    DATA_TTL: int | None = None


class BotSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False
    )

    TOKEN: str
