from aiogram import Router, F
from states import FormStartMenu
import keyboards as kb
from func import GenTask
from aiogram.fsm.context import FSMContext
from db import Data
from aiogram.types import (
    Message,
    ReplyKeyboardRemove
)

router = Router()
gentask = GenTask()
data = Data()


@router.message(FormStartMenu.start_cmd, F.text == 'Тесты')
async def main_exam(msg: Message, state: FSMContext):
    await state.set_state(FormStartMenu.exam_physic)
    await msg.answer('Тесты по темам\n'
                     ' ➥ Приборы\n'
                     ' ➥ Формулы\n'
                     ' ➥ Ученые',
                     reply_markup=kb.kb_exam
                     )


@router.message(FormStartMenu.exam_physic, F.text == 'Отмена')
async def cmd_cancel(msg: Message, state: FSMContext):
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
