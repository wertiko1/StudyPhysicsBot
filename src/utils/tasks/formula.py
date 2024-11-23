import json
import random
from typing import Tuple, Dict, List


class FormulaTask:
    def __init__(self, formula_image: str, description: str, elements_image: str) -> None:
        self.formula_image = formula_image
        self.description = description
        self.elements_image = elements_image


class GeneratedTask:
    def __init__(self, description: str, formula_image: str, answer_label: str) -> None:
        self.description = description
        self.formula_image = formula_image
        self.answer_label = answer_label

    def __repr__(self) -> str:
        return f"GeneratedTask(description='{self.description}', formula_image='{self.formula_image}', answer_label='{self.answer_label}')"


class DataLoader:
    def __init__(self, file_path: str) -> None:
        self.data = self._load_json(file_path)

    @staticmethod
    def _load_json(file_path: str) -> Dict[str, str]:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)


class FormulaTaskProvider:
    def __init__(self, formulas_path: str = 'assets/data/formulas.json',
                 elements_path: str = 'assets/data/elements.json') -> None:
        self.formulas = DataLoader(formulas_path).data
        self.elements = DataLoader(elements_path).data

    def get_random_task(self) -> Tuple[str, str]:
        """
        Возвращает случайное задание (формула, описание).
        """
        random_key = random.choice(list(self.formulas.keys()))
        formula_image = self.formulas[random_key]
        return formula_image, random_key

    def get_formula_task(self, description: str) -> FormulaTask:
        """
        Возвращает объект FormulaTask для заданного описания.
        """
        formula_image = self.formulas.get(description)
        elements_image = self.elements.get(description)

        if not formula_image or not elements_image:
            raise ValueError(f"Description '{description}' not found.")

        return FormulaTask(formula_image, description, elements_image)

    def generate_tasks(self) -> List[GeneratedTask]:
        """
        Генерирует список задач с ответами.

        Возвращает список из кортежей (описание, имя файла формулы, буква ответа).
        """
        lst = []
        lst_abc = ['A', 'B', 'C']
        used_keys = set()

        for label in lst_abc:
            while True:
                key = random.choice(list(self.formulas.keys()))
                if key not in used_keys:
                    lst.append(GeneratedTask(key, self.formulas[key], label))
                    used_keys.add(key)
                    break

        return lst
