from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.utils import Keyboard
from src.utils.states import TheoryState, MainState
from src.utils.tasks import TheoryTaskProvider

router = Router()
theory_provider = TheoryTaskProvider()


@router.message(MainState.FLASHCARD, F.text == 'Ученые')
async def start_flash_theory(msg: Message, state: FSMContext) -> None:
    await state.set_state(TheoryState.BEGIN_FLASH)
    task = theory_provider.get_random_task()
    await state.update_data(author=task.description)

    await msg.answer(
        text=task.theory,
        reply_markup=Keyboard.flip()
    )


@router.message(TheoryState.BEGIN_FLASH, F.text == 'Перевернуть')
async def send_flash_theory(msg: Message, state: FSMContext) -> None:
    data = await state.get_data()
    current_author = data.get('author')

    await msg.answer(text=current_author)
    task = theory_provider.get_random_task()
    await state.update_data(author=task.description)

    await msg.answer(
        text=task.theory,
        reply_markup=Keyboard.flip()
    )


@router.message(TheoryState.BEGIN_FLASH, F.text == 'Закончить')
async def finish_flash_theory(msg: Message, state: FSMContext) -> None:
    await state.set_state(MainState.FLASHCARD)

    await msg.answer(
        "Выберите тему карточек:",
        reply_markup=Keyboard.themes()
    )
