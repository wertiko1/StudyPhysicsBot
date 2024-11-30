import random

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    Message,
    FSInputFile,
    KeyboardButton,
    ReplyKeyboardRemove,
    ReplyKeyboardMarkup
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from src.utils import Keyboard
from src.utils.db_util import TaskType, update_task_count
from src.utils.states import MainState, FormularState
from src.utils.tasks import FormulaTaskProvider

router = Router()
formula_provider = FormulaTaskProvider()


def create_task_keyboard(tasks) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    for task in tasks:
        builder.add(KeyboardButton(text=task.answer_label))
    builder.adjust(3)
    builder.row(KeyboardButton(text='Закончить'))
    return builder.as_markup(resize_keyboard=True)


async def send_task_with_images(msg: Message, tasks):
    for task in tasks:
        photo = FSInputFile(f"./assets/formulas/{task.formula_image}")
        await msg.answer_photo(photo=photo, caption=task.answer_label)


@router.message(MainState.EXAM, F.text == 'Формулы')
async def start_exam_formula(msg: Message, state: FSMContext):
    await state.set_state(FormularState.BEGIN_EXAM)

    formula_tasks = formula_provider.generate_tasks()
    await send_task_with_images(msg, formula_tasks)

    answer_task = random.choice(formula_tasks)
    await state.update_data(
        task=answer_task.description,
        answer=answer_task.answer_label,
        count=0,
        count_valid=0
    )

    keyboard = create_task_keyboard(formula_tasks)
    await msg.answer(
        text=f"Какая формула находит:\n ● {answer_task.description}",
        reply_markup=keyboard
    )


@router.message(FormularState.BEGIN_EXAM, F.text != 'Закончить')
async def process_exam_response(msg: Message, state: FSMContext):
    results = await state.get_data()
    user_answer = msg.text

    if user_answer == results.get('answer'):
        await msg.answer("Правильно! ✅")
        await update_task_count(msg.from_user.id, TaskType.FORMULA)
        await update_task_count(msg.from_user.id, TaskType.VALID_FORMULA)
        results['count_valid'] += 1
    else:
        await msg.answer("Неправильно. ❌")
        await update_task_count(msg.from_user.id, TaskType.FORMULA)

    results['count'] += 1

    formula_tasks = formula_provider.generate_tasks()
    await send_task_with_images(msg, formula_tasks)

    answer_task = random.choice(formula_tasks)
    await state.update_data(
        task=answer_task.description,
        answer=answer_task.answer_label,
        count=results.get('count'),
        count_valid=results.get('count_valid')
    )

    keyboard = create_task_keyboard(formula_tasks)
    await msg.answer(
        text=f"Какая формула находит:\n ● {answer_task.description}",
        reply_markup=keyboard
    )


@router.message(FormularState.BEGIN_EXAM, F.text == 'Закончить')
async def cancel_exam(msg: Message, state: FSMContext):
    results = await state.get_data()
    await msg.answer(
        text=(
            f"Тест завершён ✅\n"
            f"Всего формул: {results['count']}\n"
            f"Правильно: {results['count_valid']}\n"
        ),
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(MainState.EXAM)
    await msg.answer(
        'Тесты по темам\n'
        ' ● Приборы\n'
        ' ● Формулы\n'
        ' ● Ученые',
        reply_markup=Keyboard.themes()
    )
