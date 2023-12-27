from aiogram.fsm.state import State, StatesGroup


class FormStartMenu(StatesGroup):
    start_cmd = State()
    stats = State()
    card_physic = State()
    exam_physic = State()


# состояния физика
class FormPhysic(StatesGroup):
    begin_formuls = State()
    begin_teor = State()
    begin_instr = State()


# состояния тесты
class FormPhysicExam(StatesGroup):
    begin_exam = State()
    begin_teor = State()
    begin_device = State()


# состояния статистика
class FormStats(StatesGroup):
    stats = State()
