from aiogram.fsm.state import State, StatesGroup


class MainState(StatesGroup):
    START = State()
    EXAM = State()
    MATH = State()
    FLASHCARD = State()
    STATISTIC = State()
