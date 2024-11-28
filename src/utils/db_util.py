from dataclasses import dataclass
from enum import Enum
from typing import Optional

from tortoise.exceptions import DoesNotExist
from loguru import logger

from src.models import User


@dataclass
class TaskStats:
    instrument_tasks: int
    valid_instrument_tasks: int
    theory_tasks: int
    valid_theory_tasks: int
    formula_tasks: int
    valid_formula_tasks: int
    math_tasks: int
    valid_math_tasks: int


class TaskType(Enum):
    INSTRUMENT = "instrument_tasks"
    VALID_INSTRUMENT = "valid_instrument_tasks"
    THEORY = "theory_tasks"
    VALID_THEORY = "valid_theory_tasks"
    FORMULA = "formula_tasks"
    VALID_FORMULA = "valid_formula_tasks"
    MATH = "math_tasks"
    VALID_MATH = "valid_math_tasks"


async def fetch_user(user_id: int) -> Optional[User]:
    logger.debug(f"Fetching user with ID: {user_id}")
    user = await User.filter(user_id=user_id).first()
    if user:
        logger.info(f"User with ID {user_id} found.")
    else:
        logger.warning(f"User with ID {user_id} not found.")
    return user


async def create_new_user(user_id: int) -> User:
    logger.debug(f"Creating a new user with ID: {user_id}")
    user = await User.create(
        user_id=user_id,
        max_streak=0,
        current_streak=0,
        last_session=None,
        instrument_tasks=0,
        theory_tasks=0,
        formula_tasks=0,
        math_tasks=0,
        valid_instrument_tasks=0,
        valid_theory_tasks=0,
        valid_formula_tasks=0,
        valid_math_tasks=0
    )
    logger.info(f"User with ID {user_id} successfully created.")
    return user


async def fetch_task_stats(user_id: int) -> Optional[TaskStats]:
    logger.debug(f"Fetching task statistics for user ID: {user_id}")
    try:
        user = await User.get(user_id=user_id)
        stats = TaskStats(
            instrument_tasks=user.instrument_tasks,
            valid_instrument_tasks=user.valid_instrument_tasks,
            theory_tasks=user.theory_tasks,
            valid_theory_tasks=user.valid_theory_tasks,
            formula_tasks=user.formula_tasks,
            valid_formula_tasks=user.valid_formula_tasks,
            math_tasks=user.math_tasks,
            valid_math_tasks=user.valid_math_tasks,
        )
        logger.info(f"Task statistics for user ID {user_id}: {stats}")
        return stats
    except DoesNotExist:
        logger.error(f"User with ID {user_id} not found.")
        return None


async def update_task_count(user_id: int, task_type: TaskType) -> None:
    logger.debug(f"Updating task count for user ID: {user_id}, Task Type: {task_type}")
    try:
        user = await User.get(user_id=user_id)
        field_name = task_type.value
        current_value = getattr(user, field_name)
        setattr(user, field_name, current_value + 1)
        await user.save()
        logger.info(
            f"Field '{field_name}' updated: {current_value} -> {current_value + 1} for user ID {user_id}.")
    except DoesNotExist:
        logger.error(f"User with ID {user_id} not found. Task update aborted.")


async def get_user_task_percentile(user_id: int) -> Optional[float]:
    logger.debug(f"Calculating task percentile for user ID: {user_id}")

    try:
        user = await User.get(user_id=user_id)

        user_task_count = (
                user.instrument_tasks +
                user.valid_instrument_tasks +
                user.theory_tasks +
                user.valid_theory_tasks +
                user.formula_tasks +
                user.valid_formula_tasks +
                user.math_tasks +
                user.valid_math_tasks
        )

        all_users = await User.all()
        if not all_users:
            logger.warning("No users found in the database.")
            return None

        total_users = len(all_users)

        lower_task_count = sum(
            1 for u in all_users if (
                    u.instrument_tasks +
                    u.valid_instrument_tasks +
                    u.theory_tasks +
                    u.valid_theory_tasks +
                    u.formula_tasks +
                    u.valid_formula_tasks +
                    u.math_tasks +
                    u.valid_math_tasks
            ) < user_task_count
        )
        percentile = (lower_task_count / total_users) * 100
        logger.info(f"User ID {user_id} is better than {percentile:.2f}% of users.")
        return percentile

    except DoesNotExist:
        logger.error(f"User with ID {user_id} not found.")
        return None
