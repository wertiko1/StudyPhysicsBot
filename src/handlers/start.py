from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from src.utils import Keyboard, MessageManager
from src.utils.db_util import fetch_user, create_new_user
from src.utils.states import MainState

router = Router()


@router.message(CommandStart())
async def start(msg: types.Message, state: FSMContext) -> None:
    user = await fetch_user(msg.from_user.id)
    await state.set_state(MainState.START)
    if not user:
        await create_new_user(msg.from_user.id)
        await MessageManager.greeting(msg, Keyboard.main())
    else:
        await MessageManager.main(msg, Keyboard.main())
