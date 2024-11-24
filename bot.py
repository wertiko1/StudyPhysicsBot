import asyncio
from loguru import logger
from aiogram import Bot, Dispatcher
from src.utils.setup.logging import LogSetup
from src.utils.setup.bot import BotSetup
from src.utils.setup.commands import BotCommands
from src.utils.setup.routers import RoutersLoader
from src.utils.setup.db import SetupData
from configs.config_reader import Config
from configs.settings import CacheSettings


async def on_startup(bot: Bot, dispatcher: Dispatcher) -> None:
    logger.info("Running startup tasks...")
    await db.get_db_client().startup()
    await db.get_redis_client().get_client()
    RoutersLoader(routers_path='src/handlers', dp=dispatcher).load()
    await bot.set_my_commands(
        BotCommands().get_commands_list()
    )
    await bot.delete_webhook(drop_pending_updates=True)
    logger.info("Startup tasks complete")


async def on_shutdown(bot: Bot, dispatcher: Dispatcher) -> None:
    logger.info("Running shutdown tasks...")
    await db.get_db_client().shutdown()
    await dispatcher.storage.close()
    logger.info("Shutdown tasks complete")


def main() -> None:
    LogSetup()
    logger.info("Starting bot...")

    bot_setup = BotSetup(
        token=Config.TOKEN,
        parse_mode="HTML",
        redis_client=db.get_redis_client().get_client(),
        state_ttl=CacheSettings.state_ttl,
        data_ttl=CacheSettings.data_ttl
    )

    bot = bot_setup.get_bot()
    dispatcher = bot_setup.get_dispatcher()

    dispatcher.startup.register(on_startup)
    dispatcher.shutdown.register(on_shutdown)

    try:
        asyncio.run(dispatcher.start_polling(bot))
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped")


if __name__ == "__main__":
    db = SetupData()
    main()
