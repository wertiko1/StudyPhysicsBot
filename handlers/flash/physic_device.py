from aiogram import Router, F
from func import GenTask
from states import FormPhysic
from aiogram.fsm.context import FSMContext
from states import FormStartMenu
import keyboards as kb
from data import Data
from aiogram.types import Message

# экземпляр класса
router = Router()
gentask = GenTask()
data = Data()

# повторение приборов
@router.message(FormStartMenu.card_physic, F.text == 'Приборы')
async def cmd_physic_instr(msg: Message, state: FSMContext):
    await state.set_state(FormPhysic.begin_instr)
    instr, prim = gentask.physic_instr()
    await state.update_data(prim=prim)
    await msg.answer(text=instr, reply_markup=kb.kb_flip)

# цикл приборы
@router.message(FormPhysic.begin_instr, F.text == 'Перевернуть')
async def send_instr(msg: Message, state: FSMContext):
    prim = await state.get_data()
    data.add_stats(msg.from_user.id, 'device_flash')
    await msg.answer(text=prim['prim'])
    instr, prim = gentask.physic_instr()
    await state.update_data(prim=prim)
    await msg.answer(text=instr)

# команда закончить
@router.message(FormPhysic.begin_instr, F.text == 'Закончить')
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