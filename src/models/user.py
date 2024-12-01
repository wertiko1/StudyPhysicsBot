from tortoise import fields
from tortoise.models import Model


class User(Model):
    user_id = fields.BigIntField(unique=True)
    timezone = fields.TimeField()

    max_streak = fields.IntField(default=0)
    current_streak = fields.IntField(default=0)

    last_session = fields.DateField(null=True)
