from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis



class BotSetup:
    def __init__(self, token: str, parse_mode: str, redis_client: Redis, state_ttl: int, data_ttl: int) -> None:
        self._bot = Bot(
            token=token,
            default=DefaultBotProperties(parse_mode=parse_mode)
        )
        self._storage = RedisStorage(
            redis=redis_client,
            state_ttl=state_ttl,
            data_ttl=data_ttl
        )
        self._dispatcher = Dispatcher(storage=self._storage)

    def get_bot(self) -> Bot:
        return self._bot

    def get_dispatcher(self) -> Dispatcher:
        return self._dispatcher
