import random
from typing import List

from .loader import DataLoader


class FormulaTask:
    def __init__(self, formula_image: str, elements_image: str, description: str, answer_label: str = None) -> None:
        self.formula_image = formula_image
        self.elements_image = elements_image
        self.description = description
        self.answer_label = answer_label

    def __repr__(self) -> str:
        return f"FormulaTask(formula_image='{self.formula_image}', elements_image='{self.elements_image}' description='{self.description}', answer_label='{self.answer_label}')"


class FormulaTaskProvider:
    def __init__(self, formulas_path: str = 'assets/data/formulas.json',
                 elements_path: str = 'assets/data/elements.json') -> None:
        self.formulas = DataLoader(formulas_path).data
        self.elements = DataLoader(elements_path).data

    def get_random_task(self) -> FormulaTask:
        description = random.choice(list(self.formulas.keys()))
        formula_image = self.formulas[description]
        elements_image = self.elements.get(description)
        return FormulaTask(formula_image, elements_image, description)

    def get_formula_task(self, description: str) -> FormulaTask:
        formula_image = self.formulas.get(description)
        elements_image = self.elements.get(description)

        if not formula_image or not elements_image:
            raise ValueError(f"Description '{description}' not found.")

        return FormulaTask(formula_image, elements_image, description)

    def generate_tasks(self) -> List[FormulaTask]:
        tasks = []
        labels = ['A', 'B', 'C']
        used_descriptions = set()

        for label in labels:
            while True:
                description = random.choice(list(self.formulas.keys()))
                if description not in used_descriptions:
                    tasks.append(
                        FormulaTask(self.formulas[description], self.elements[description], description, label))
                    used_descriptions.add(description)
                    break

        return tasks
