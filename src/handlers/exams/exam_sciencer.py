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
from src.utils.states import MainState, TheoryState
from src.utils.tasks import SciencerTaskProvider, SciencerTask

import random

router = Router()
sciencer_provider = SciencerTaskProvider()


def create_task_keyboard(tasks) -> ReplyKeyboardBuilder:
    builder = ReplyKeyboardBuilder()
    for task in tasks:
        builder.add(KeyboardButton(text=task.description))
    builder.adjust(3)
    builder.row(KeyboardButton(text="Закончить"))
    return builder


@router.message(MainState.EXAM, F.text == "Ученые")
async def start_exam_theory(msg: Message, state: FSMContext):
    await state.set_state(TheoryState.BEGIN_EXAM)

    tasks = sciencer_provider.generate_tasks()
    answer_task: SciencerTask = random.choice(tasks)

    await state.update_data(
        task=answer_task.sciencer,
        answer=answer_task.description,
        count=0,
        count_correct=0,
    )

    keyboard = create_task_keyboard(tasks)
    await msg.answer(
        text=f"Какой ученый открыл:\n ● {answer_task.sciencer}",
        reply_markup=keyboard.as_markup(resize_keyboard=True),
    )


@router.message(TheoryState.BEGIN_EXAM, F.text != "Закончить")
async def process_exam_theory(msg: Message, state: FSMContext):
    data = await state.get_data()
    user_answer = msg.text

    count = data["count"] + 1
    count_correct = data["count_correct"]

    await update_task_count(msg.from_user.id, TaskType.THEORY)

    if user_answer == data["answer"]:
        await msg.answer("Правильно! ✅")
        count_correct += 1
        await update_task_count(msg.from_user.id, TaskType.VALID_THEORY)
    else:
        await msg.answer("Неправильно. ❌")

    tasks = sciencer_provider.generate_tasks()
    answer_task: SciencerTask = random.choice(tasks)

    await state.update_data(
        task=answer_task.sciencer,
        answer=answer_task.description,
        count=count,
        count_correct=count_correct,
    )

    keyboard = create_task_keyboard(tasks)
    await msg.answer(
        text=f"Какой ученый открыл:\n ● {answer_task.sciencer}",
        reply_markup=keyboard.as_markup(resize_keyboard=True),
    )


@router.message(TheoryState.BEGIN_EXAM, F.text == "Закончить")
async def finish_exam_theory(msg: Message, state: FSMContext):
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
