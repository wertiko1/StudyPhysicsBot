from aiogram import Router, F
from func import GenTask
from aiogram.fsm.context import FSMContext
from states import FormPhysic
import keyboards as kb
from data import Data
from aiogram.types import Message
from states import FormStartMenu

# экземпляр класса
router = Router()
gentask = GenTask()
data = Data()

# повторение ученых
@router.message(FormStartMenu.card_physic, F.text == 'Ученые')
async def cmd_physic_teor(msg: Message, state: FSMContext):
    await state.set_state(FormPhysic.begin_teor)
    teor, author = gentask.physic_teor()
    await state.update_data(author=author)
    await msg.answer(text=teor, reply_markup=kb.kb_flip)

# цикл ученые
@router.message(FormPhysic.begin_teor, F.text == 'Перевернуть')
async def send_teor(msg: Message, state: FSMContext):
    author = await state.get_data()
    await msg.answer(text=author['author'])
    data.add_stats(msg.from_user.id, 'teor_flash')
    teor, author = gentask.physic_teor()
    await state.update_data(author=author)
    await msg.answer(text=teor)

# команда закончить
@router.message(FormPhysic.begin_teor, F.text == 'Закончить')
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
