from tortoise import fields
from tortoise.models import Model


class User(Model):
    user_id = fields.BigIntField(unique=True)

    max_streak = fields.IntField(default=0)
    current_streak = fields.IntField(default=0)

    last_session = fields.DateField(null=True)

    instrument_tasks = fields.IntField(default=0)
    theory_tasks = fields.IntField(default=0)
    formula_tasks = fields.IntField(default=0)
    math_tasks = fields.IntField(default=0)

    valid_instrument_tasks = fields.IntField(default=0)
    valid_theory_tasks = fields.IntField(default=0)
    valid_formula_tasks = fields.IntField(default=0)
    valid_math_tasks = fields.IntField(default=0)
