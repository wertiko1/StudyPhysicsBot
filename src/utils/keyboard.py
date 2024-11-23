from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from typing import List


def _create(buttons: List[List[str]], resize: bool = True, placeholder: str = None) -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=btn) for btn in row] for row in buttons],
        resize_keyboard=resize,
        input_field_placeholder=placeholder
    )
    return keyboard


class Keyboard:
    @staticmethod
    def main() -> ReplyKeyboardMarkup:
        buttons = [
            ['Карточки', 'Тесты', 'Устный счет'],
            ['Статистика']
        ]
        return _create(buttons, placeholder='Выберите действие')

    @staticmethod
    def answer() -> ReplyKeyboardMarkup:
        buttons = [['Да', 'Нет']]
        return _create(buttons, placeholder='Вы готовы?')

    @staticmethod
    def cancel() -> ReplyKeyboardMarkup:
        buttons = [['Отмена']]
        return _create(buttons, placeholder='Нажмите для отмены')

    @staticmethod
    def stop() -> ReplyKeyboardMarkup:
        buttons = [['Закончить']]
        return _create(buttons, placeholder='Нажмите, чтобы закончить')

    @staticmethod
    def flip() -> ReplyKeyboardMarkup:
        buttons = [['Перевернуть'], ['Закончить']]
        return _create(buttons, placeholder='Выберите действие')

    @staticmethod
    def themes() -> ReplyKeyboardMarkup:
        buttons = [
            ['Формулы', 'Ученые', 'Приборы'],
            ['Отмена']
        ]
        return _create(buttons, placeholder='Выберите тему работы')
