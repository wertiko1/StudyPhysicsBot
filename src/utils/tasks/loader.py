import json
from typing import Dict


class DataLoader:
    def __init__(self, file_path: str) -> None:
        self.data = self._load_json(file_path)

    @staticmethod
    def _load_json(file_path: str) -> Dict[str, str]:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
