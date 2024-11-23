from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.utils.states import MainState
from src.utils import Keyboard

router = Router()


@router.message(MainState.START, F.text == 'Карточки')
async def main_flash_command(msg: Message, state: FSMContext):
    await state.set_state(MainState.FLASHCARD)
    await msg.answer(
        'Выберите тему карточек',
        reply_markup=Keyboard.themes()
    )


@router.message(MainState.FLASHCARD, F.text == 'Отмена')
async def flash_cancel(msg: Message, state: FSMContext):
    await state.set_state(MainState.START)
    await msg.answer(
        f"Привет {msg.from_user.username}! 😊"
    )
    await msg.answer(
        "Я рад приветствовать тебя! 📚🌱\n"
        "Здесь ты найдешь разнообразные задания, формулы,"
        " которые помогут тебе расширить свои знания! 📝💡\n"
    )
    await msg.answer(
        "Это только первая версия. 🚀\nЕсли у тебя возникнут идеи или предложения "
        "по улучшению моей работы, "
        "не стесняйся делиться ими!\nРазработчик @wertikomoment"
    )
    await msg.answer(
        "Мои команды:\n"
        " ● /start - Главное меню\n"
        " ● /cancel - Отмена действия\n",
        reply_markup=Keyboard.themes()
    )
