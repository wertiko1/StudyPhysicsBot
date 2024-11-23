from aiogram.fsm.state import State, StatesGroup


class MainState(StatesGroup):
    START = State()
    EXAM = State()
    MATH = State()
    FLASHCARD = State()
    STATISTIC = State()


class StatisticState(StatesGroup):
    pass


class FormularState(StatesGroup):
    BEGIN_FLASH = State()
    BEGIN_EXAM = State()


class InstrumentState(StatesGroup):
    BEGIN_FLASH = State()
    BEGIN_EXAM = State()


class TheoryState(StatesGroup):
    BEGIN_FLASH = State()
    BEGIN_EXAM = State()
