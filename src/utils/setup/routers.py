from aiogram import Router, Dispatcher
from typing import List
from loguru import logger

from src.handlers import start_router


class Routers:
    def __init__(self) -> None:
        self._routers: List[Router] = [
            start_router
        ]

    async def include_routers(self, dp: Dispatcher) -> None:
        dp.include_routers(*self._routers)
        logger.info('Routers included')
