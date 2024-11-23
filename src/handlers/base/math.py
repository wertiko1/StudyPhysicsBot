from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from src.utils.states import MainState, MathState
from src.utils.db_util import TaskType, update_task_count
from src.utils.tasks import MathTaskProvider
from src.utils import Keyboard

router = Router()
math_provider = MathTaskProvider()


async def send_greeting(msg: Message) -> None:
    await msg.answer(f"Привет, {msg.from_user.username}! 😊")
    await msg.answer(
        "Я рад приветствовать тебя! 📚🌱\n"
        "Здесь ты найдешь разнообразные задания, формулы, которые помогут тебе погрузиться "
        "в мир физики и расширить свои знания! 📝💡"
    )
    await msg.answer(
        "Это только первая версия. 🚀\nЕсли у тебя возникнут идеи или предложения по улучшению моей работы, "
        "не стесняйся делиться ими!\nРазработчик: @wertikomoment."
    )
    await msg.answer(
        "Мои команды:\n"
        " ● /start - Главное меню\n"
        " ● /cancel - Отмена действия\n",
        reply_markup=Keyboard.main()
    )


@router.message(MainState.START, F.text == 'Устный счет')
async def equation_mentally_start(msg: Message, state: FSMContext) -> None:
    await state.set_state(MathState.BEGIN)
    await msg.answer("Вы готовы?", reply_markup=Keyboard.answer())


@router.message(MathState.BEGIN)
async def start_math_task(msg: Message, state: FSMContext) -> None:
    if msg.text == "Да":
        math_task = math_provider.generate_task()
        await state.update_data(answer=math_task.answer, task=math_task.equation)
        await msg.answer(
            f"Реши в уме:\n{math_task.equation}",
            reply_markup=Keyboard.cancel()
        )
        await state.set_state(MathState.RECURSION)
    elif msg.text == "Нет":
        await state.set_state(MainState.START)
        await send_greeting(msg)
    else:
        await msg.answer("Пожалуйста, ответьте 'Да' или 'Нет'.")


@router.message(MathState.RECURSION)
async def send_math_task(msg: Message, state: FSMContext) -> None:
    if msg.text.isdigit():
        user_data = await state.get_data()
        user_answer = int(msg.text)

        if user_answer == user_data.get("answer"):
            await msg.answer("Правильно! ✅")
            await update_task_count(msg.from_user.id, TaskType.MATH)
            await update_task_count(msg.from_user.id, TaskType.VALID_MATH)
            math_task = math_provider.generate_task()
            await state.update_data(answer=math_task.answer, task=math_task.equation)
            await msg.answer(f"Реши в уме:\n{math_task.equation}")
        else:
            await msg.answer(f"Неправильно, попробуй еще раз:\n{user_data.get('task')}")
            await update_task_count(msg.from_user.id, TaskType.MATH)
    elif msg.text == "Закончить":
        await cmd_cancel(msg, state)
    else:
        await msg.answer("Введите число!")


@router.message(MathState.RECURSION, F.text == "Закончить")
async def math_cancel(msg: Message, state: FSMContext) -> None:
    await state.set_state(MainState.START)
    await send_greeting(msg)
