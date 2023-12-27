from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from states import FormStartMenu, FormStats
from func import GenTask
import keyboards as kb
from data import Data
from aiogram.types import Message

# экземпляр классов
router = Router()
gentask = GenTask()
data = Data()

# команда статистики
@router.message(FormStartMenu.start_cmd, F.text == 'Статистика')
async def stats(msg: Message, state: FSMContext):
    await state.set_state(FormStartMenu.stats)
    await msg.answer('Выберите раздел',
                     reply_markup=kb.kb_stats
                     )

# роутер общая статистика
@router.message(FormStartMenu.stats, F.text == 'Общая статистика')
async def stats_general(msg: Message, state: FSMContext):
    await state.set_state(FormStats.stats)
    result = data.get_stats(msg.from_user.id)
    flash = result[0][3] + result[0][5] + result[0][7]
    exam = result[0][4] + result[0][6] + result[0][8]
    procent = data.get_users_proc(msg.from_user.id)
    await msg.answer(f"Общая статистика\n"
                     f"Всего карточек: {flash}\n"
                     f"Всего тестов: {exam}\n"
                     f"Устный счет: {result[0][2]}\n"
                     f"Это на {procent}% лучше чем у других пользователей",
                     reply_markup=kb.kb_cncl
                     )

# роутер тесты
@router.message(FormStartMenu.stats, F.text == 'Тесты')
async def stats_exam(msg: Message, state: FSMContext):
    await state.set_state(FormStats.stats)
    result = data.get_stats(msg.from_user.id)
    s = result[0][4] + result[0][6] + result[0][8]
    await msg.answer(f'Тестов выполнено {s}\n'
                     f'Тестов по приборам {result[0][10]}/{result[0][4]}\n'
                     f'Тестов по ученым {result[0][12]}/{result[0][6]}\n'
                     f'Тестов по формулам {result[0][11]}/{result[0][8]}\n'
                     f'Правильно/Всего',
                     reply_markup=kb.kb_cncl)

# роутер карточки
@router.message(FormStartMenu.stats, F.text == 'Карточки')
async def stats_flash(msg: Message, state: FSMContext):
    await state.set_state(FormStats.stats)
    result = data.get_stats(msg.from_user.id)
    s = result[0][3] + result[0][5] + result[0][7]
    await msg.answer(f'Всего карточек {s}\n'
                     f'Карточек по приборам {result[0][3]}\n'
                     f'Карточек по ученым {result[0][5]}\n'
                     f'Карточек по формулам {result[0][7]}',
                     reply_markup=kb.kb_cncl)

# роутер устный счет
@router.message(FormStartMenu.stats, F.text == 'Устный счет')
async def stats_math(msg: Message, state: FSMContext):
    await state.set_state(FormStats.stats)
    results = data.get_stats(msg.from_user.id)
    await msg.answer(f'Попыток {results[0][9]}\n'
                     f'Решено правильно {results[0][2]}',
                     reply_markup=kb.kb_cncl)

# роутер закончить
@router.message(FormStats.stats, F.text == 'Отмена')
async def cmd_cancel(msg: Message, state: FSMContext):
    await state.set_state(FormStartMenu.stats)
    await msg.answer('Выберите раздел',
                     reply_markup=kb.kb_stats
                     )

# роутер отмены
@router.message(FormStartMenu.stats, F.text == 'Отмена')
async def cmd_cancel(msg: Message, state: FSMContext):
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