import random
from typing import List

from .loader import DataLoader


class InstrumentTask:
    def __init__(self, instrument: str, purpose: str) -> None:
        self.instrument = instrument
        self.purpose = purpose

    def __repr__(self) -> str:
        return f"InstrumentTask(instrument='{self.instrument}', purpose='{self.purpose}')"


class InstrumentTaskProvider:
    def __init__(self, data_path: str = 'assets/data/instruments.json') -> None:
        self.instruments = DataLoader(data_path).data

    def get_random_task(self) -> InstrumentTask:
        instrument = random.choice(list(self.instruments.keys()))
        purpose = self.instruments[instrument]
        return InstrumentTask(instrument, purpose)

    def generate_tasks(self) -> List[InstrumentTask]:
        tasks = []
        used_instruments = set()

        for _ in range(3):
            while True:
                instrument = random.choice(list(self.instruments.keys()))
                if instrument not in used_instruments:
                    tasks.append(InstrumentTask(instrument, self.instruments[instrument]))
                    used_instruments.add(instrument)
                    break

        return tasks
