from aiogram import Router, F
from aiogram.fsm.context import FSMContext

from src.keyboards import Keyboard
from src.utils.states import FormularState, MainState
from src.utils.tasks import FormulaTaskProvider

from aiogram.types import (
    Message,
    FSInputFile
)

router = Router()
formula_provider = FormulaTaskProvider()


@router.message(MainState.FLASHCARD, F.text == 'Формулы')
async def start_flash_formulas(msg: Message, state: FSMContext) -> None:
    await state.set_state(FormularState.BEGIN_FLASH)
    filename, task = formula_provider.get_random_task()
    await state.update_data(task=task)
    await msg.answer(
        text=task,
        reply_markup=Keyboard.flip()
    )


@router.message(FormularState.BEGIN_FLASH, F.text == 'Перевернуть')
async def send_flash_formulas(msg: Message, state: FSMContext) -> None:
    task = await state.get_data()
    formula_task = formula_provider.get_formula_task(task['task'])
    photo = FSInputFile(f"./assets/formulas/{formula_task.formula_image}",
                        filename=f"{formula_task.formula_image[:-4]}")
    await msg.answer_photo(photo=photo)
    photo = FSInputFile(f"./assets/formulas/{formula_task.elements_image}",
                        filename=f"{formula_task.elements_image[:-4]}")
    await msg.answer_photo(photo=photo)
    filename, task = formula_provider.get_random_task()
    await state.update_data(task=task)
    await msg.answer(text=task)


@router.message(FormularState.BEGIN_FLASH, F.text == 'Закончить')
async def finish_flash_formulas(msg: Message, state: FSMContext) -> None:
    await state.set_state(MainState.FLASHCARD)
    await msg.answer(
        'Выберите тему карточек',
        reply_markup=Keyboard.themes()
    )
