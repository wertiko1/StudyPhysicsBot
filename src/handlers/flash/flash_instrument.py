from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from src.utils import Keyboard
from src.utils.states import InstrumentState, MainState
from src.utils.tasks import InstrumentTaskProvider

router = Router()
instrument_provider = InstrumentTaskProvider()


@router.message(MainState.FLASHCARD, F.text == 'Приборы')
async def start_flash_instrument(msg: Message, state: FSMContext) -> None:
    await state.set_state(InstrumentState.BEGIN_FLASH)
    instrument_task = instrument_provider.get_random_task()
    await state.update_data(answer=instrument_task.instrument)

    await msg.answer(
        text=instrument_task.purpose,
        reply_markup=Keyboard.flip()
    )


@router.message(InstrumentState.BEGIN_FLASH, F.text == 'Перевернуть')
async def send_flash_instrument(msg: Message, state: FSMContext) -> None:
    data = await state.get_data()
    current_answer = data.get('answer')

    if current_answer:
        await msg.answer(text=current_answer)
    instrument_task = instrument_provider.get_random_task()
    await state.update_data(answer=instrument_task.instrument)

    await msg.answer(
        text=instrument_task.purpose,
        reply_markup=Keyboard.flip()
    )


@router.message(InstrumentState.BEGIN_FLASH, F.text == 'Закончить')
async def finish_flash_instrument(msg: Message, state: FSMContext) -> None:
    await state.set_state(MainState.FLASHCARD)

    await msg.answer(
        'Выберите тему карточек:',
        reply_markup=Keyboard.themes()
    )
