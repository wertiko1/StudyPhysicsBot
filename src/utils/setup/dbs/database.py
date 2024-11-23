from tortoise import Tortoise
from configs.config_reader import Config


class DataBase:
    def __init__(self) -> None:
        self.__db = Config.MYSQL_URL

    async def startup(self) -> None:
        await Tortoise.init(
            db_url=self.__db,
            modules={
                'models': ['src.models']
            }
        )
        await Tortoise.generate_schemas()

    async def shutdown(self) -> None:
        await Tortoise.close_connections()
