from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.utils import Keyboard, MessageManager
from src.utils.states import MainState

router = Router()


@router.message(MainState.START, F.text == 'Тесты')
async def main_exam_command(msg: Message, state: FSMContext):
    await state.set_state(MainState.EXAM)
    await msg.answer(
        'Тесты по темам\n'
        ' ● Приборы\n'
        ' ● Формулы\n'
        ' ● Ученые',
        reply_markup=Keyboard.themes()
    )


@router.message(MainState.EXAM, F.text == 'Отмена')
async def exam_cancel(msg: Message, state: FSMContext):
    await state.set_state(MainState.START)
    await MessageManager.main(msg, Keyboard.main())
