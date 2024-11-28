from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile

from src.utils import Keyboard
from src.utils.states import FormularState, MainState
from src.utils.tasks import FormulaTaskProvider

router = Router()
formula_provider = FormulaTaskProvider()


@router.message(MainState.FLASHCARD, F.text == 'Формулы')
async def start_flash_formulas(msg: Message, state: FSMContext) -> None:
    await state.set_state(FormularState.BEGIN_FLASH)
    formula_task = formula_provider.get_random_task()
    await state.update_data(task=formula_task.description)

    await msg.answer(
        text=formula_task.description,
        reply_markup=Keyboard.flip()
    )


@router.message(FormularState.BEGIN_FLASH, F.text == 'Перевернуть')
async def send_flash_formulas(msg: Message, state: FSMContext) -> None:
    data = await state.get_data()
    current_task = data.get('task')

    formula_task = formula_provider.get_formula_task(current_task)

    formula_photo = FSInputFile(
        f"./assets/formulas/{formula_task.formula_image}",
        filename=formula_task.formula_image[:-4]
    )
    await msg.answer_photo(photo=formula_photo)

    elements_photo = FSInputFile(
        f"./assets/formulas/{formula_task.elements_image}",
        filename=formula_task.elements_image[:-4]
    )
    await msg.answer_photo(photo=elements_photo)

    formula_task = formula_provider.get_random_task()
    await state.update_data(task=formula_task.description)

    await msg.answer(
        text=formula_task.description,
        reply_markup=Keyboard.flip()
    )


@router.message(FormularState.BEGIN_FLASH, F.text == 'Закончить')
async def finish_flash_formulas(msg: Message, state: FSMContext) -> None:
    await state.set_state(MainState.FLASHCARD)

    await msg.answer(
        "Выберите тему карточек:",
        reply_markup=Keyboard.themes()
    )
