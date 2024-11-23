from aiogram import Router, F
from aiogram.filters.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from func import GenTask
import keyboards as kb
from db import Data
from aiogram.types import (
    Message
)

router = Router()
gentask = GenTask()
data = Data()


class MathItems(StatesGroup):
    begin = State()
    math_recurs = State()


@router.message(FormStartMenu.start_cmd, F.text == 'Устный счет')
async def equation_mentally_start(msg: Message, state: FSMContext):
    await state.set_state(MathItems.begin)
    await msg.answer('Вы готовы?', reply_markup=kb.kb_answer)


@router.message(MathItems.begin)
async def math_gettask(msg: Message, state: FSMContext):
    if msg.text == 'Да':
        equation = gentask.math_task()
        await msg.answer(f'Реши в уме\n{equation[0]}', reply_markup=kb.kb_cancel)
        await state.update_data(answer=equation[1], task=equation[0])
        await state.set_state(MathItems.math_recurs)
    elif msg.text == 'Нет':
        await state.set_state(FormStartMenu.start_cmd)
        await msg.answer(f"Привет {msg.from_user.username}! 😊")
        await msg.answer("Я рад приветствовать тебя! 📚🌱\n"
                         "Здесь ты найдешь разнообразные задания, формулы,"
                         " которые помогут тебе погрузиться в мир физики и расширить свои знания! 📝💡\n"
                         )
        await msg.answer("Это только первая версия. 🚀\nЕсли у тебя возникнут идеи или предложения "
                         "по улучшению моей работы, "
                         "не стесняйся делиться ими!\nРазработчик @wertikomoment."
                         )
        await msg.answer("Мои команды:\n"
                         " ● /start - Главное меню\n"
                         " ● /cancel - Отмена действия\n"
                         "P.S. команду /cancel использовать в любой непонятной ситуации",
                         reply_markup=kb.kb_main
                         )
    else:
        await msg.answer('Что?')


@router.message(MathItems.math_recurs)
async def math_task(msg: Message, state: FSMContext):
    result = await state.get_data()
    if msg.text.isdigit():
        if int(msg.text) == result['answer']:
            equation = gentask.math_task()
            await msg.answer('Правильно!')
            data.add_stats(msg.from_user.id, 'task1')
            data.add_stats(msg.from_user.id, 'math_task')
            await msg.answer(f'Реши в уме\n{equation[0]}')
            await state.update_data(answer=equation[1], task=equation[0])
        else:
            result = result['task']
            await msg.answer(f'Неправильно, ещё раз\n{result}')
            data.add_stats(msg.from_user.id, 'task1')
    elif msg.text == 'Закончить':
        await state.set_state(FormStartMenu.start_cmd)
        await msg.answer(f"Привет {msg.from_user.username}! 😊")
        await msg.answer("Я рад приветствовать тебя! 📚🌱\n"
                         "Здесь ты найдешь разнообразные задания, формулы,"
                         " которые помогут тебе погрузиться в мир физики и расширить свои знания! 📝💡\n"
                         )
        await msg.answer("Это только первая версия. 🚀\nЕсли у тебя возникнут идеи или предложения "
                         "по улучшению моей работы, "
                         "не стесняйся делиться ими!\nРазработчик @wertikomoment."
                         )
        await msg.answer("Мои команды:\n"
                         " ● /start - Главное меню\n"
                         " ● /cancel - Отмена действия\n"
                         "P.S. команду /cancel использовать в любой непонятной ситуации",
                         reply_markup=kb.kb_main
                         )
    else:
        await msg.answer('Введите число!')


@router.message(MathItems.math_recurs, F.text == 'Закончить')
async def cmd_cancel(msg: Message, state: FSMContext):
    await state.set_state(FormStartMenu.start_cmd)
    await msg.answer(f"Привет {msg.from_user.username}! 😊")
    await msg.answer("Я рад приветствовать тебя! 📚🌱\n"
                     "Здесь ты найдешь разнообразные задания, формулы,"
                     " которые помогут тебе расширить свои знания! 📝💡\n"
                     )
    await msg.answer("Это только первая версия. 🚀\nЕсли у тебя возникнут идеи или предложения "
                     "по улучшению моей работы, "
                     "не стесняйся делиться ими!\nРазработчик @wertikomoment."
                     )
    await msg.answer("Мои команды:\n"
                     " ● /start - Главное меню\n"
                     " ● /cancel - Отмена действия\n"
                     "P.S. команду /cancel использовать в любой непонятной ситуации",
                     reply_markup=kb.kb_main
                     )
