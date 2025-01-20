from loguru import logger
from tortoise import Tortoise
from src.settings import db


class DataBase:
    def __init__(self) -> None:
        pass

    async def startup(self) -> None:
        await Tortoise.init(
            db_url=db.url,
            modules={
                'models': db.DB_MODELS
            }
        )
        await Tortoise.generate_schemas()
        logger.info('Database connected')

    async def shutdown(self) -> None:
        await Tortoise.close_connections()
