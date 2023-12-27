from aiogram import Router, F
from func import GenTask
from aiogram.fsm.context import FSMContext
from states import FormStartMenu
import keyboards as kb
from aiogram.types import Message

# экземпляр класса
router = Router()
gentask = GenTask()


# команда карточки
@router.message(FormStartMenu.start_cmd, F.text == 'Карточки')
async def cmd_physic(msg: Message, state: FSMContext):
    await state.set_state(FormStartMenu.card_physic)
    await msg.answer('Выберите тему карточек',
                     reply_markup=kb.kb_exam
                     )

# команда отмены
@router.message(FormStartMenu.card_physic, F.text == 'Отмена')
async def cancel(msg: Message, state: FSMContext):
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
                     reply_markup=kb.kb_main
                     )