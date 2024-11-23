from loguru import logger

from apscheduler.schedulers.background import BackgroundScheduler


class TaskScheduler:
    def __init__(self, interval: int) -> None:
        self.interval = interval

    def handler(self) -> None:
        pass


class Scheduler(BackgroundScheduler):
    def __init__(self) -> None:
        self._task = TaskScheduler(60)
        super().__init__()

    def add_tasks(self) -> None:
        self.add_job(self._task.handler, "interval", seconds=self._task.interval, args=[self._task])
        logger.info('Database check started')
