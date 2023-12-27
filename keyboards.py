from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup
)

# клавиатура да/нет
keyboard_get_answer = [
    [
        KeyboardButton(text='Да'),
        KeyboardButton(text='Нет')
    ]
]
kb_answer = ReplyKeyboardMarkup(keyboard=keyboard_get_answer,
                                resize_keyboard=True,
                                input_field_placeholder="Вы готовы?"
                                )

# клавиатура закончить
keyboard_get_cancel = [
    [
        KeyboardButton(text='Закончить')
    ]
]
kb_cancel = ReplyKeyboardMarkup(keyboard=keyboard_get_cancel,
                                resize_keyboard=True,
                                input_field_placeholder="Нажмите чтобы закончить"
                                )

# клавиатура отмены
keyboard_get_cncl = [
    [
        KeyboardButton(text='Отмена')
    ]
]
kb_cncl = ReplyKeyboardMarkup(keyboard=keyboard_get_cncl,
                              resize_keyboard=True,
                              input_field_placeholder="Нажмите для отмены"
                              )

# клавиатура перевернуть
keyboard_flip = [
    [
        KeyboardButton(text='Перевернуть')
    ],
    [
        KeyboardButton(text='Закончить')
    ]
]
kb_flip = ReplyKeyboardMarkup(keyboard=keyboard_flip,
                              resize_keyboard=True,
                              input_field_placeholder='Выберите действие'
                              )

keyboard_get_exam = [
    [
        KeyboardButton(text='Формулы'),
        KeyboardButton(text='Ученые'),
        KeyboardButton(text='Приборы')
    ],
    [
        KeyboardButton(text='Отмена')
    ]
]
kb_exam = ReplyKeyboardMarkup(keyboard=keyboard_get_exam,
                              resize_keyboard=True,
                              input_field_placeholder='Выберите тему работы'
                              )

# клавиатура глобального меню
keyboard_main_menu = [
    [
        KeyboardButton(text='Карточки'),
        KeyboardButton(text='Тесты'),
        KeyboardButton(text='Устный счет'),
    ],
    [
        KeyboardButton(text='Статистика')
    ]
]
kb_main = ReplyKeyboardMarkup(keyboard=keyboard_main_menu,
                              resize_keyboard=True,
                              input_field_placeholder='Выберите действие'
                              )

# клавиатура статистики
keyboard_get_stats = [
    [
        KeyboardButton(text='Общая статистика')
    ],
    [
        KeyboardButton(text='Тесты'),
        KeyboardButton(text='Карточки'),
        KeyboardButton(text='Устный счет')
    ],
    [
        KeyboardButton(text='Отмена')
    ]
]
kb_stats = ReplyKeyboardMarkup(keyboard=keyboard_get_stats,
                               resize_keyboard=True,
                               input_field_placeholder='Выберите действие'
                               )
