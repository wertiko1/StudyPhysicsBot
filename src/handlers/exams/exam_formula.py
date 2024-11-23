from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    Message,
    FSInputFile,
    KeyboardButton,
    ReplyKeyboardRemove
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from src.utils.states import MainState, FormularState
from src.utils.tasks import FormulaTaskProvider
import random

router = Router()
task_provider = FormulaTaskProvider()
builder = ReplyKeyboardBuilder()


@router.message(MainState.EXAM, F.text == 'Формулы')
async def start_exam_formula(msg: Message, state: FSMContext):
    await state.set_state(FormularState.BEGIN_EXAM)

    tasks = task_provider.generate_tasks()

    for task in tasks:
        photo = FSInputFile(f"./assets/formulas/{task.formula_image}", filename=(task.formula_image)[:-4])
        await msg.answer_photo(caption=task.answer_label, photo=photo)
        builder.add(KeyboardButton(text=task.answer_label))

    builder.adjust(3)
    builder.row(KeyboardButton(text='Закончить'))

    answer_task = random.choice(tasks)
    await state.update_data(
        task=answer_task.description,
        answer=answer_task.answer_label,
        count=0,
        count_valid=0
    )

    await msg.answer(
        text=f"Какая формула находит:\n ● {answer_task.description}",
        reply_markup=builder.as_markup(resize_keyboard=True)
    )


@router.message(FormularState.BEGIN_EXAM, F.text != 'Закончить')
async def send_exam_formula(msg: Message, state: FSMContext):
    results = await state.get_data()
    user_answer = msg.text

    if user_answer == results['answer']:
        await msg.answer('Правильно')
        data.add_stats(msg.from_user.id, 'form_exam')
        data.add_stats(msg.from_user.id, 'task3')
        results['count_valid'] += 1
    else:
        await msg.answer('Неправильно')
        data.add_stats(msg.from_user.id, 'form_exam')

    results['count'] += 1

    tasks = task_provider.generate_tasks()

    for task in tasks:
        photo = FSInputFile(f"./assets/formulas/{task.formula_image}", filename=(task.formula_image)[:-4])
        await msg.answer_photo(caption=task.answer_label, photo=photo)
        builder.add(KeyboardButton(text=task.answer_label))

    builder.adjust(3)
    builder.row(KeyboardButton(text='Закончить'))

    answer_task = random.choice(tasks)
    await state.update_data(
        task=answer_task.description,
        answer=answer_task.answer_label,
        count=results['count'],
        count_valid=results['count_valid']
    )

    await msg.answer(
        text=f"Какая формула находит:\n ● {answer_task.description}",
        reply_markup=builder.as_markup(resize_keyboard=True)
    )


@router.message(FormularState.BEGIN_EXAM, F.text == 'Закончить')
async def cancel(msg: Message, state: FSMContext):
    results = await state.get_data()
    await msg.answer(
        f"Тест завершен\n"
        f"Всего формул: {results['count']}\n"
        f"Правильно: {results['count_valid']}\n"
        "Главное меню /start",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.clear()
