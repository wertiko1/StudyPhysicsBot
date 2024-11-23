from aiogram.fsm.state import State, StatesGroup


class MainState(StatesGroup):
    START = State()
    EXAM = State()
    MATH = State()
    FLASHCARD = State()
    STATISTIC = State()


class FormularState(StatesGroup):
    BEGIN_FLASH = State()
    BEGIN_EXAM = State()


class InstrumentState(StatesGroup):
    BEGIN_FLASH = State()
    BEGIN_EXAM = State()


class TheoryState(StatesGroup):
    BEGIN_FLASH = State()
    BEGIN_EXAM = State()


class MathState(StatesGroup):
    BEGIN = State()
    RECURSION = State()
