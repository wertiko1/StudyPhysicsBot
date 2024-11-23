from aiogram.types import Message, ReplyKeyboardMarkup
from typing import List


class MessageObj:
    def __init__(self, text: str, reply_kb: ReplyKeyboardMarkup | None) -> None:
        self.text = text
        self.reply_kb = reply_kb


async def _send_messages(messages: List[MessageObj], msg: Message) -> None:
    for message in messages:
        await msg.answer(
            message.text,
            reply_markup=message.reply_kb
        )


class MessageManager:
    @staticmethod
    async def greeting(message: Message, keyboard: ReplyKeyboardMarkup = None):
        await _send_messages(
            messages=[
                MessageObj(
                    text="Я рад приветствовать тебя! 📚🌱\n"
                         "Здесь ты найдешь разнообразные задания, формулы,"
                         " которые помогут тебе расширить свои знания! 📝💡\n",
                    reply_kb=None
                ),
                MessageObj(
                    text="Это только первая версия. 🚀\nЕсли у тебя возникнут идеи или предложения "
                         "по улучшению моей работы, "
                         "не стесняйся делиться ими!\n"
                         "Разработчик @wertikomoment",
                    reply_kb=None
                ),
                MessageObj(
                    text="Мои команды:\n"
                         " ● /start - Главное меню",
                    reply_kb=keyboard
                )
            ],
            msg=message
        )

    @staticmethod
    async def main(message: Message, keyboard: ReplyKeyboardMarkup = None):
        await _send_messages(
            messages=[
                MessageObj(
                    text='Моя задача - помочь тебе в изучении физики!\n'
                         'Выбирай категорию задач',
                    reply_kb=keyboard
                )
            ],
            msg=message
        )
