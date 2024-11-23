import random
import json
from typing import List, Tuple, Dict


class TheoryTask:
    def __init__(self, theory: str, description: str, answer_label: str) -> None:
        self.theory = theory  # Название теории или открытия
        self.description = description  # Описание теории или открытия
        self.answer_label = answer_label  # Метка для правильного ответа (A, B, C)

    def __repr__(self) -> str:
        return f"TheoryTask(theory='{self.theory}', description='{self.description}', answer_label='{self.answer_label}')"


class DataLoader:
    def __init__(self, file_path: str) -> None:
        self.data = self._load_json(file_path)

    @staticmethod
    def _load_json(file_path: str) -> Dict[str, str]:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)


class TheoryTaskProvider:
    def __init__(self, data_path: str = 'assets/data/theories.json') -> None:
        self.data = DataLoader(data_path).data

    def get_random_task(self) -> TheoryTask:
        """
        Возвращает случайное задание (теория, описание).
        """
        theory = random.choice(list(self.data.keys()))
        description = self.data[theory]
        return TheoryTask(theory, description, answer_label="")

    def get_theory_task(self, theory: str) -> TheoryTask:
        """
        Возвращает объект TheoryTask для заданной теории.
        """
        description = self.data.get(theory)

        if not description:
            raise ValueError(f"Theory '{theory}' not found.")

        return TheoryTask(theory, description, answer_label="")

    def generate_tasks(self) -> List[TheoryTask]:
        """
        Генерирует список задач с ответами (A, B, C).
        """
        tasks = []
        labels = ['A', 'B', 'C']
        used_theories = set()

        for label in labels:
            while True:
                theory = random.choice(list(self.data.keys()))
                if theory not in used_theories:
                    tasks.append(TheoryTask(theory, self.data[theory], label))
                    used_theories.add(theory)
                    break

        return tasks
