from aiogram import Router, F
from func import GenTask
from states import FormStartMenu
from states import FormPhysicExam
from aiogram.fsm.context import FSMContext
from db import Data
import random as rn
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import (
    Message,
    KeyboardButton,
    ReplyKeyboardRemove
)

router = Router()


@router.message(FormStartMenu.exam_physic, F.text == 'Ученые')
async def cmd_exam_form(msg: Message, state: FSMContext):
    await state.set_state(FormPhysicExam.begin_teor)
    builder = ReplyKeyboardBuilder()
    result = gentask.gen_teor()
    lst = []
    for i in range(3):
        lst.append(result[i][1])
        builder.add(KeyboardButton(text=result[i][1]))
    builder.adjust(3)
    builder.row(KeyboardButton(text='Закончить'))
    answer, count, count_p = rn.choice(lst), 0, 0
    for i in range(3):
        if result[i][1] == answer:
            task = result[i][0]
            break
    await state.update_data(task=task, answer=answer, count=count, count_p=count_p)
    await msg.answer(text=f"Кто открыл:\n ● {task}", reply_markup=builder.as_markup(resize_keyboard=True))


@router.message(FormPhysicExam.begin_teor, F.text != 'Закончить')
async def rout_task(msg: Message, state: FSMContext):
    results = await state.get_data()
    if msg.text == results['answer']:
        await msg.answer('Правильно')
        data.add_stats(msg.from_user.id, 'teor_exam')
        data.add_stats(msg.from_user.id, 'task4')
        c = results['count']
        c += 1
        cp = results['count_p']
        cp += 1
        builder = ReplyKeyboardBuilder()
        result = gentask.gen_teor()
        lst = []
        for i in range(3):
            lst.append(result[i][1])
            builder.add(KeyboardButton(text=result[i][1]))
        builder.adjust(3)
        builder.row(KeyboardButton(text='Закончить'))
        answer, count, count_p = rn.choice(lst), 0, 0
        for i in range(3):
            if result[i][1] == answer:
                task = result[i][0]
                break
        await state.update_data(task=task, answer=answer, count=c, count_p=cp)
        await msg.answer(text=f"Кто открыл:\n ● {task}",
                         reply_markup=builder.as_markup(resize_keyboard=True))
    else:
        await msg.answer('Неправильно')
        data.add_stats(msg.from_user.id, 'teor_exam')
        c = results['count']
        c += 1
        cp = results['count_p']
        builder = ReplyKeyboardBuilder()
        result = gentask.gen_teor()
        lst = []
        for i in range(3):
            lst.append(result[i][1])
            builder.add(KeyboardButton(text=result[i][1]))
        builder.adjust(3)
        builder.row(KeyboardButton(text='Закончить'))
        answer, count, count_p = rn.choice(lst), 0, 0
        for i in range(3):
            if result[i][1] == answer:
                task = result[i][0]
                break
        await state.update_data(task=task, answer=answer, count=c, count_p=cp)
        await msg.answer(text=f"Какая формула находит:\n ● {task}",
                         reply_markup=builder.as_markup(resize_keyboard=True))


@router.message(FormPhysicExam.begin_teor, F.text == 'Закончить')
async def cmd_cancel(msg: Message, state: FSMContext):
    result = await state.get_data()
    await msg.answer(f"Тест завершен\n"
                     f"Всего: {result['count']}\n"
                     f"Правильно: {result['count_p']}\n"
                     "Главное меню /start",
                     reply_markup=ReplyKeyboardRemove()
                     )
    await state.clear()
