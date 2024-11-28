from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.utils.states import MainState
from src.utils import Keyboard, MessageManager

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
    await MessageManager.main(msg, Keyboard.main())
