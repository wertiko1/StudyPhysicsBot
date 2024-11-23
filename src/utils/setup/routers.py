from aiogram import Router, Dispatcher
from typing import List
from loguru import logger

from src.handlers import (
    start_router,
    stats_router,
    flash_router,
    exam_router,
    math_router,
    exam_theory_router,
    exam_formula_router,
    exam_instrument_router,
    flash_theory_router,
    flash_formula_router,
    flash_instrument_router
)


class Routers:
    def __init__(self) -> None:
        self._routers: List[Router] = [
            start_router,
            stats_router,
            flash_router,
            exam_router,
            math_router,
            exam_theory_router,
            exam_formula_router,
            exam_instrument_router,
            flash_theory_router,
            flash_formula_router,
            flash_instrument_router
        ]

    async def include_routers(self, dp: Dispatcher) -> None:
        dp.include_routers(*self._routers)
        logger.info('Routers included')
