from aiogram import Router, F
from aiogram.types import Message

from src.utils import Keyboard
from src.utils.db_util import get_user_task_percentile, fetch_task_stats
from src.utils.states import MainState

router = Router()


@router.message(MainState.START, F.text == 'Статистика')
async def stats(msg: Message) -> None:
    user_stats = await fetch_task_stats(msg.from_user.id)
    percent = await get_user_task_percentile(msg.from_user.id)
    total_exams = user_stats.theory_tasks + user_stats.formula_tasks + user_stats.instrument_tasks
    total_exams_valid = user_stats.valid_formula_tasks + user_stats.valid_instrument_tasks + user_stats.valid_theory_tasks
    await msg.answer(
        f"Статистика\n"
        f"Всего тестов: {total_exams}\n"
        f" ● Правильно: {total_exams_valid}\n\n"
        f"Устный счет: {user_stats.math_tasks}\n"
        f" ● Правильно: {user_stats.valid_math_tasks}\n\n"
        f"Это на {int(percent)}% лучше чем у других пользователей",
        reply_markup=Keyboard.main()
    )
