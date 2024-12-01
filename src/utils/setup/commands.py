from typing import Tuple, List

from aiogram.types import BotCommand


class Command:
    def __init__(self, name: str, description: str) -> None:
        self.name = name
        self.description = description


class BotCommands:
    def __init__(self) -> None:
        self._bot_commands_str: List[Tuple[str, str]] = [
            ("start", "Запустить бота"),
            ("help", "Помощь"),
            ("about", "О боте")
        ]

        self._bot_commands_list: List[Command] = [
            Command(command_str[0], command_str[1])
            for command_str in self._bot_commands_str
        ]

        self._bot_commands = [
            BotCommand(
                command=command.name,
                description=command.description
            ) for command in self._bot_commands_list
        ]

    def get_commands_list(self) -> List[BotCommand]:
        return self._bot_commands

    def get_command_str(self) -> List[Tuple[str, str]]:
        return self._bot_commands_str
