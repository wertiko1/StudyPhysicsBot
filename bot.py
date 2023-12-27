import asyncio
from aiogram import Bot, Dispatcher, Router
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.enums.parse_mode import ParseMode
from aiogram.client.bot import BotCommand
from aiogram.filters import Command
from states import FormStartMenu
from aiogram.fsm.context import FSMContext
import handlers.flash.physics
import handlers.flash.physic_teor
import handlers.flash.physic_device
import handlers.flash.physic_formuls
import handlers.math
import handlers.exams.form_exam
import handlers.exams.exam_main
import handlers.exams.teor_exam
import handlers.exams.device_exam
import handlers.stats.statistics
import logging
import keyboards
from data import Data
import config
from func import GenTask
from aiogram.types import (
    Message,
    ReplyKeyboardRemove
)
# логирование
logger = logging.getLogger(__name__)

# создать экземпляры классов
data = Data()
router = Router()
gentask = GenTask()

#команды
async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Главное меню"),
        BotCommand(command="/cancel", description="Отмена")
    ]
    await bot.set_my_commands(commands)
# главное меню
@router.message(Command(commands=['start']))
async def cmd_start(msg: Message, state: FSMContext):
    await state.set_state(FormStartMenu.start_cmd)
    await msg.answer(f"Привет {msg.from_user.username}! 😊")
    await msg.answer("Я рад приветствовать тебя! 📚🌱\n"
                     "Здесь ты найдешь разнообразные задания, формулы,"
                     " которые помогут тебе расширить свои знания! 📝💡\n"
                     )
    await msg.answer("Это только первая версия. 🚀\nЕсли у тебя возникнут идеи или предложения "
                     "по улучшению моей работы, "
                     "не стесняйся делиться ими!\nРазработчик @wertikomoment."
                     )
    await msg.answer("Мои команды:\n"
                     " ● /start - Главное меню\n"
                     " ● /cancel - Отмена действия\n"
                     "P.S. команду /cancel использовать в любой непонятной ситуации",
                     reply_markup=keyboards.kb_main
                     )
    data.add_user(msg.from_user.id, msg.from_user.username)

# команда отмены
@router.message(Command(commands=['cancel']))
async def cmd_cancel(msg: Message, state: FSMContext):
    await state.clear()
    await msg.answer("Действие отменено", reply_markup=ReplyKeyboardRemove())

# конфигурация запуска
async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logger.error("Starting bot")

    bot = Bot(token=config.token, parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_routers(router,
                       handlers.flash.physics.router,
                       handlers.flash.physic_formuls.router,
                       handlers.flash.physic_device.router,
                       handlers.flash.physic_teor.router,
                       handlers.math.router,
                       handlers.exams.exam_main.router,
                       handlers.exams.device_exam.router,
                       handlers.exams.teor_exam.router,
                       handlers.exams.form_exam.router,
                       handlers.stats.statistics.router
                       )
    data.create_table()

    await set_commands(bot)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

# точка входа
if __name__ == "__main__":
    asyncio.run(main())