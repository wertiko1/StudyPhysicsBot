from aiogram.fsm.state import State, StatesGroup


class InstrumentState(StatesGroup):
    BEGIN_FLASH = State()
    BEGIN_EXAM = State()


class TheoryState(StatesGroup):
    BEGIN_FLASH = State()
    BEGIN_EXAM = State()


class MathState(StatesGroup):
    BEGIN = State()
    RECURSION = State()


class FormularState(StatesGroup):
    BEGIN_FLASH = State()
    BEGIN_EXAM = State()
