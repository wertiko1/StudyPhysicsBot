from aiogram import Router, F
from func import GenTask
from states import FormPhysic
from aiogram.fsm.context import FSMContext
from states import FormStartMenu
import keyboards as kb
from data import Data
from aiogram.types import (
    Message,
    FSInputFile
)

# экземпляр класса
router = Router()
gentask = GenTask()
data = Data()

# повторение формул
@router.message(FormStartMenu.card_physic, F.text == 'Формулы')
async def cmd_physic_form(msg: Message, state: FSMContext):
    await state.set_state(FormPhysic.begin_formuls)
    filename, task = gentask.physic_form()
    await state.update_data(task=task)
    await msg.answer(text=task, reply_markup=kb.kb_flip)

# цикл формулы
@router.message(FormPhysic.begin_formuls, F.text == 'Перевернуть')
async def send_form(msg: Message, state: FSMContext):
    task = await state.get_data()
    data.add_stats(msg.from_user.id, 'form_flash')
    filename, task, filename_elem = gentask.search_form(task['task'])
    photo = FSInputFile(f"./formuls/{filename}", filename=f"{filename[:-4]}")
    await msg.answer_photo(photo=photo)
    photo = FSInputFile(f"./formuls/{filename_elem}", filename=f"{filename_elem[:-4]}")
    await msg.answer_photo(photo=photo)
    filename, task = gentask.physic_form()
    await state.update_data(task=task)
    await msg.answer(text=task)

# команда закончить
@router.message(FormPhysic.begin_formuls, F.text == 'Закончить')
async def cmd_finish(msg: Message, state: FSMContext):
    await state.set_state(FormStartMenu.card_physic)
    await msg.answer('Выберите тему карточек',
                     reply_markup=kb.kb_exam
                     )

# команда закончить
@router.message(FormStartMenu.card_physic, F.text == 'Закончить')
async def cmd_finish(msg: Message, state: FSMContext):
    await state.set_state(FormStartMenu.card_physic)
    await msg.answer('Выберите тему карточек',
                     reply_markup=kb.kb_exam
                     )