from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    Message,
    KeyboardButton,
    ReplyKeyboardRemove
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from src.utils import Keyboard
from src.utils.db_util import TaskType, update_task_count
from src.utils.states import MainState, InstrumentState
from src.utils.tasks import InstrumentTaskProvider, InstrumentTask

import random

router = Router()
instrument_provider = InstrumentTaskProvider()


def create_task_keyboard(tasks) -> ReplyKeyboardBuilder:
    builder = ReplyKeyboardBuilder()
    for task in tasks:
        builder.add(KeyboardButton(text=task.instrument))
    builder.adjust(3)
    builder.row(KeyboardButton(text="Закончить"))
    return builder


@router.message(MainState.EXAM, F.text == "Приборы")
async def start_exam_instrument(msg: Message, state: FSMContext):
    await state.set_state(InstrumentState.BEGIN_EXAM)

    tasks = instrument_provider.generate_tasks()
    answer_task: InstrumentTask = random.choice(tasks)

    await state.update_data(
        task=answer_task.purpose,
        answer=answer_task.instrument,
        count=0,
        count_correct=0,
    )

    keyboard = create_task_keyboard(tasks)
    await msg.answer(
        text=f"Какой прибор используется для:\n ● {answer_task.purpose}",
        reply_markup=keyboard.as_markup(resize_keyboard=True),
    )


@router.message(InstrumentState.BEGIN_EXAM, F.text != "Закончить")
async def process_exam_instrument(msg: Message, state: FSMContext):
    data = await state.get_data()
    user_answer = msg.text

    count = data.get("count") + 1
    count_correct = data.get("count_correct")

    if user_answer == data.get("answer"):
        await msg.answer("Правильно! ✅")
        count_correct += 1
        await update_task_count(msg.from_user.id, TaskType.INSTRUMENT)
        await update_task_count(msg.from_user.id, TaskType.VALID_INSTRUMENT)
    else:
        await msg.answer("Неправильно. ❌")
        await update_task_count(msg.from_user.id, TaskType.INSTRUMENT)

    tasks = instrument_provider.generate_tasks()
    answer_task: InstrumentTask = random.choice(tasks)

    await state.update_data(
        task=answer_task.purpose,
        answer=answer_task.instrument,
        count=count,
        count_correct=count_correct,
    )

    keyboard = create_task_keyboard(tasks)
    await msg.answer(
        text=f"Какой прибор используется для:\n ● {answer_task.purpose}",
        reply_markup=keyboard.as_markup(resize_keyboard=True),
    )


@router.message(InstrumentState.BEGIN_EXAM, F.text == "Закончить")
async def finish_exam_instrument(msg: Message, state: FSMContext):
    data = await state.get_data()
    await msg.answer(
        text=(
            f"Тест завершён ✅\n"
            f"Всего вопросов: {data.get('count')}\n"
            f"Правильных ответов: {data.get('count_correct')}\n"
        ),
        reply_markup=ReplyKeyboardRemove(),
    )
    await state.set_state(MainState.EXAM)
    await msg.answer(
        'Тесты по темам\n'
        ' ● Приборы\n'
        ' ● Формулы\n'
        ' ● Ученые',
        reply_markup=Keyboard.themes()
    )
