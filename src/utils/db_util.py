from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional

from loguru import logger
from pytz import timezone
from tortoise.exceptions import DoesNotExist

from src.models import User, FormulaTask, TheoryTask, MathTask, InstrumentTask


@dataclass
class TaskCountsByDay:
    instrument_tasks: Dict[datetime.date, int]
    theory_tasks: Dict[datetime.date, int]
    formula_tasks: Dict[datetime.date, int]
    math_tasks: Dict[datetime.date, int]

    @property
    def total_task_counts(self) -> Dict[datetime.date, int]:
        total_counts = defaultdict(int)

        for date, count in self.instrument_tasks.items():
            total_counts[date] += count
        for date, count in self.theory_tasks.items():
            total_counts[date] += count
        for date, count in self.formula_tasks.items():
            total_counts[date] += count
        for date, count in self.math_tasks.items():
            total_counts[date] += count

        return dict(total_counts)


@dataclass
class TasksByDay:
    instrument_tasks: List[InstrumentTask]
    theory_tasks: List[TheoryTask]
    formula_tasks: List[FormulaTask]
    math_tasks: List[MathTask]

    @property
    def all_tasks(self) -> List:
        return (
                self.instrument_tasks +
                self.theory_tasks +
                self.formula_tasks +
                self.math_tasks
        )

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

    @property
    def summary_valid_stats(self) -> int:
        result = self.valid_theory_tasks + self.valid_formula_tasks + self.valid_instrument_tasks
        return result

    @property
    def summary_stats(self) -> int:
        result = self.theory_tasks + self.formula_tasks + self.instrument_tasks
        return result


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
    user = await User.filter(user_id=user_id).first()
    if user:
        logger.info(f"User with ID {user_id} found.")
    else:
        logger.warning(f"User with ID {user_id} not found.")
    return user



async def create_new_user(user_id: int) -> User:
    user = await User.create(
        user_id=user_id,
        max_streak=0,
        current_streak=0,
        last_session=None,
        group=None
    )
    logger.info(f"User with ID {user_id} successfully created.")
    return user



async def fetch_task_stats(user_id: int) -> Optional[TaskStats]:
    try:
        user = await User.get(user_id=user_id)

        stats = TaskStats(
            instrument_tasks=await InstrumentTask.filter(user=user).count(),
            valid_instrument_tasks=await InstrumentTask.filter(user=user, is_correct=True).count(),
            theory_tasks=await TheoryTask.filter(user=user).count(),
            valid_theory_tasks=await TheoryTask.filter(user=user, is_correct=True).count(),
            formula_tasks=await FormulaTask.filter(user=user).count(),
            valid_formula_tasks=await FormulaTask.filter(user=user, is_correct=True).count(),
            math_tasks=await MathTask.filter(user=user).count(),
            valid_math_tasks=await MathTask.filter(user=user, is_correct=True).count(),
        )
        logger.info(f"Task statistics for user ID {user_id}: {stats}")
        return stats
    except DoesNotExist:
        logger.error(f"User with ID {user_id} not found.")
        return None


async def update_task_count(user_id: int, task_type: TaskType, is_correct: bool = False) -> None:
    try:
        user = await User.get(user_id=user_id)

        if task_type == TaskType.INSTRUMENT:
            await InstrumentTask.create(user=user, completed_at=datetime.now(), is_correct=is_correct)
        elif task_type == TaskType.THEORY:
            await TheoryTask.create(user=user, completed_at=datetime.now(), is_correct=is_correct)
        elif task_type == TaskType.FORMULA:
            await FormulaTask.create(user=user, completed_at=datetime.now(), is_correct=is_correct)
        elif task_type == TaskType.MATH:
            await MathTask.create(user=user, completed_at=datetime.now(), is_correct=is_correct)
        else:
            logger.error(f"Invalid task type: {task_type}")
            return

        user.last_session = datetime.now()
        await user.save()

        logger.info(
            f"Task of type {task_type} updated for user ID {user_id}. Correct: {is_correct}. "
            f"Last session updated to {user.last_session}."
        )
    except DoesNotExist:
        logger.error(f"User with ID {user_id} not found. Task update aborted.")


async def get_user_task_percentile(user_id: int) -> Optional[float]:
    try:
        user = await User.get(user_id=user_id)

        user_task_count = (
                await InstrumentTask.filter(user=user).count() +
                await TheoryTask.filter(user=user).count() +
                await FormulaTask.filter(user=user).count() +
                await MathTask.filter(user=user).count()
        )

        all_users = await User.all()
        if not all_users:
            logger.warning("No users found in the database.")
            return None

        total_users = len(all_users)

        lower_task_count = sum(
            1 for other_user in all_users if (
                    await InstrumentTask.filter(user=other_user).count() +
                    await TheoryTask.filter(user=other_user).count() +
                    await FormulaTask.filter(user=other_user).count() +
                    await MathTask.filter(user=other_user).count()
            ) < user_task_count
        )

        lower_task_count = 1 if not lower_task_count else lower_task_count
        percentile = (lower_task_count / total_users) * 100
        logger.info(f"User ID {user_id} is better than {percentile:.2f}% of users.")
        return percentile

    except DoesNotExist:
        logger.error(f"User with ID {user_id} not found.")
        return None


async def save_task(user_id: int, task_name: TaskType, is_correct: bool = False):
    try:
        user = await User.get(user_id=user_id)
        now_utc = datetime.now()

        if task_name == TaskType.INSTRUMENT:
            await InstrumentTask.create(user=user, completed_at=now_utc, is_correct=is_correct)
        elif task_name == TaskType.THEORY:
            await TheoryTask.create(user=user, completed_at=now_utc, is_correct=is_correct)
        elif task_name == TaskType.THEORY:
            await FormulaTask.create(user=user, completed_at=now_utc, is_correct=is_correct)
        elif task_name == TaskType.MATH:
            await MathTask.create(user=user, completed_at=now_utc, is_correct=is_correct)
        else:
            logger.error(f"Invalid task name: {task_name}")
            raise ValueError(f"Invalid task name: {task_name}")

        user.last_session = now_utc
        await user.save()

        logger.info(f"Task {task_name} saved for user ID {user_id}. Correct: {is_correct}.")
    except DoesNotExist:
        logger.error(f"User with ID {user_id} not found. Task save aborted.")


async def get_tasks_for_user_by_day(user_id: int, target_date: datetime.date) -> TasksByDay:
    try:
        logger.debug(f"Fetching tasks for user ID {user_id} on date {target_date}.")

        user = await User.get(user_id=user_id)
        user_tz = timezone(user.timezone or "UTC")
        logger.info(f"User with ID {user_id} found. Using timezone {user.timezone or 'UTC'}.")

        start_of_day = datetime.combine(target_date, datetime.min.time(), tzinfo=user_tz)
        end_of_day = start_of_day + timedelta(days=1)

        start_of_day_utc = start_of_day.astimezone(timezone("UTC"))
        end_of_day_utc = end_of_day.astimezone(timezone("UTC"))

        logger.debug(f"UTC range: {start_of_day_utc} - {end_of_day_utc}.")

        instrument_tasks = await InstrumentTask.filter(
            user=user, completed_at__gte=start_of_day_utc, completed_at__lt=end_of_day_utc
        ).all()

        theory_tasks = await TheoryTask.filter(
            user=user, completed_at__gte=start_of_day_utc, completed_at__lt=end_of_day_utc
        ).all()

        formula_tasks = await FormulaTask.filter(
            user=user, completed_at__gte=start_of_day_utc, completed_at__lt=end_of_day_utc
        ).all()

        math_tasks = await MathTask.filter(
            user=user, completed_at__gte=start_of_day_utc, completed_at__lt=end_of_day_utc
        ).all()

        logger.info(
            f"Fetched {len(instrument_tasks)} instrument, "
            f"{len(theory_tasks)} theory, {len(formula_tasks)} formula, "
            f"{len(math_tasks)} math tasks for user ID {user_id} on {target_date}."
        )

        return TasksByDay(
            instrument_tasks=instrument_tasks,
            theory_tasks=theory_tasks,
            formula_tasks=formula_tasks,
            math_tasks=math_tasks,
        )

    except DoesNotExist:
        logger.error(f"User with ID {user_id} not found. Cannot fetch tasks.")
        return TasksByDay([], [], [], [])


async def get_task_counts_by_day(user_id: int) -> TaskCountsByDay:
    try:
        logger.debug(f"Calculating task counts by day for user ID {user_id}.")

        user = await User.get(user_id=user_id)
        logger.info(f"User with ID {user_id} found.")

        instrument_tasks = await InstrumentTask.filter(user=user).all()
        theory_tasks = await TheoryTask.filter(user=user).all()
        formula_tasks = await FormulaTask.filter(user=user).all()
        math_tasks = await MathTask.filter(user=user).all()

        task_counts_instrument = defaultdict(int)
        task_counts_theory = defaultdict(int)
        task_counts_formula = defaultdict(int)
        task_counts_math = defaultdict(int)

        for task in instrument_tasks:
            day = task.completed_at.date()
            task_counts_instrument[day] += 1

        for task in theory_tasks:
            day = task.completed_at.date()
            task_counts_theory[day] += 1

        for task in formula_tasks:
            day = task.completed_at.date()
            task_counts_formula[day] += 1

        for task in math_tasks:
            day = task.completed_at.date()
            task_counts_math[day] += 1

        logger.info(
            f"Task counts calculated for user ID {user_id}. "
            f"Instrument: {dict(task_counts_instrument)}, Theory: {dict(task_counts_theory)}, "
            f"Formula: {dict(task_counts_formula)}, Math: {dict(task_counts_math)}."
        )

        return TaskCountsByDay(
            instrument_tasks=dict(task_counts_instrument),
            theory_tasks=dict(task_counts_theory),
            formula_tasks=dict(task_counts_formula),
            math_tasks=dict(task_counts_math),
        )

    except DoesNotExist:
        logger.error(f"User with ID {user_id} not found. Cannot calculate task counts.")
        return TaskCountsByDay({}, {}, {}, {})
