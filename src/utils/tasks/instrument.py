import random
import json
from typing import List, Tuple, Dict


class InstrumentTask:
    def __init__(self, instrument: str, purpose: str, answer_label: str) -> None:
        self.instrument = instrument
        self.purpose = purpose
        self.answer_label = answer_label

    def __repr__(self) -> str:
        return f"InstrumentTask(instrument='{self.instrument}', purpose='{self.purpose}', answer_label='{self.answer_label}')"


class DataLoader:
    def __init__(self, file_path: str) -> None:
        self.data = self._load_json(file_path)

    @staticmethod
    def _load_json(file_path: str) -> Dict[str, str]:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)


class InstrumentTaskProvider:
    def __init__(self, data_path: str = 'assets/data/instruments.json') -> None:
        self.data = DataLoader(data_path).data

    def get_random_task(self) -> InstrumentTask:
        """
        Возвращает случайное задание (инструмент, назначение).
        """
        instrument = random.choice(list(self.data.keys()))
        purpose = self.data[instrument]
        return InstrumentTask(instrument, purpose, answer_label="")

    def get_instrument_task(self, instrument: str) -> InstrumentTask:
        """
        Возвращает объект InstrumentTask для заданного инструмента.
        """
        purpose = self.data.get(instrument)

        if not purpose:
            raise ValueError(f"Instrument '{instrument}' not found.")

        return InstrumentTask(instrument, purpose, answer_label="")

    def generate_tasks(self) -> List[InstrumentTask]:
        """
        Генерирует список задач с ответами.
        """
        tasks = []
        labels = ['A', 'B', 'C']
        used_instruments = set()

        for label in labels:
            while True:
                instrument = random.choice(list(self.data.keys()))
                if instrument not in used_instruments:
                    tasks.append(InstrumentTask(instrument, self.data[instrument], label))
                    used_instruments.add(instrument)
                    break

        return tasks
