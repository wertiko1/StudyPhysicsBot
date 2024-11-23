from random import choice, randint


class MathTask:
    def __init__(self, equation: str) -> None:
        self.equation = equation.replace('**', '^')
        self.answer = eval(equation)


class MathTaskProvider:
    def __init__(self) -> None:
        self._math_signs = ['*', '**']

    def generate_task(self) -> MathTask:
        sign = choice(self._math_signs)
        digit = str(randint(11, 99))
        multiplier = 2 if sign == "**" else randint(11, 99)
        equation = f"{digit} {sign} {multiplier}"
        return MathTask(equation)
