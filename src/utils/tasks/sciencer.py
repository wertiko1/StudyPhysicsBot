import random
from typing import List

from .loader import DataLoader


class SciencerTask:
    def __init__(self, sciencer: str, description: str) -> None:
        self.sciencer = sciencer
        self.description = description

    def __repr__(self) -> str:
        return f"SciencerTask(theory='{self.sciencer}', description='{self.description}')"


class SciencerTaskProvider:
    def __init__(self, data_path: str = 'assets/data/theories.json') -> None:
        self.data = DataLoader(data_path).data

    def get_random_task(self) -> SciencerTask:
        sciencer = random.choice(list(self.data.keys()))
        description = self.data[sciencer]
        return SciencerTask(sciencer, description)

    def generate_tasks(self) -> List[SciencerTask]:
        tasks = []
        used_theories = set()

        for _ in range(3):
            while True:
                sciencer = random.choice(list(self.data.keys()))
                if sciencer not in used_theories:
                    tasks.append(SciencerTask(sciencer, self.data[sciencer]))
                    used_theories.add(sciencer)
                    break

        return tasks
