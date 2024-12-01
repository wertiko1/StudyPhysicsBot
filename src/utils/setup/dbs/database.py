from loguru import logger
from tortoise import Tortoise

from configs.config_reader import Config


class DataBase:
    def __init__(self) -> None:
        self._db = Config.SQL_URL

    async def startup(self) -> None:
        await Tortoise.init(
            db_url=self._db,
            modules={
                'models': ['src.models']
            }
        )
        await Tortoise.generate_schemas()
        logger.info('Database connected')


    async def shutdown(self) -> None:
        await Tortoise.close_connections()
