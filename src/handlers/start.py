from aiogram import Router, types
from aiogram.filters import CommandStart

router = Router()


@router.message(CommandStart())
async def cmd_cancel(msg: types.Message):
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
                     "P.S. команду /cancel использовать в любой непонятной ситуации"
                     )