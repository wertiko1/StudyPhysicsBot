from dataclasses import dataclass
from datetime import time, date

from tortoise import fields
from tortoise.models import Model


class User(Model):
    user_id = fields.BigIntField()

    max_streak = fields.IntField()
    current_streak = fields.IntField()

    last_session = fields.DateField()

    instrument_tasks = fields.IntField()
    theory_tasks = fields.IntField()
    physic_tasks = fields.IntField()
    math_tasks = fields.IntField()

    valid_instrument_tasks = fields.IntField()
    valid_theory_tasks = fields.IntField()
    valid_physic_tasks = fields.IntField()
    valid_math_tasks = fields.IntField()


@dataclass
class UserData:
    user_id: int
    max_streak: int
    current_streak: int
    last_session: date
    instrument_tasks: int
    theory_tasks: int
    physic_tasks: int
    math_tasks: int
    valid_instrument_tasks: int
    valid_theory_tasks: int
    valid_physic_tasks: int
    valid_math_tasks: int
