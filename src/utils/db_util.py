import datetime
from src.models import User, UserData
from typing import Dict


async def get_user(user_id: int) -> User | None:
    user = await User.filter(user_id=user_id).first()
    return user


async def create_user(user_data: UserData) -> User:
    user = await User.create(
        user_id=user_data.user_id
    )
    return user


async def get_stats_data(user_id: int) -> Dict[datetime.datetime, int]:
    pass


async def add_stats(user_id: int) -> User:
    pass
