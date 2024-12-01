from tortoise import fields
from tortoise.models import Model


class TaskBase(Model):
    user = fields.ForeignKeyField("models.User", related_name="%(class)s_tasks")
    completed_at = fields.DatetimeField()
    is_correct = fields.BooleanField(default=False)

    class Meta:
        abstract = True


class InstrumentTask(TaskBase):
    pass


class TheoryTask(TaskBase):
    pass


class FormulaTask(TaskBase):
    pass


class MathTask(TaskBase):
    pass
