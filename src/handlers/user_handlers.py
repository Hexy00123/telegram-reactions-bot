import os
import json
import random
from time import sleep
from typing import List

from aiogram import types
from aiogram.types import Message
from aiogram import Dispatcher, html
from aiogram.filters import CommandStart


async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    print(message.chat.id)
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")


class GameMessageHandler:
    def __init__(self, *_, config_path):
        self.games, self.positive_reactions = self.__read_config(config_path)

    def __read_config(self, config_path) -> tuple:
        with open(config_path, "r") as file:
            config = json.load(file)

            games = config["games"]
            positive_reactions = config["positive_reactions"]

        return games, positive_reactions

    def process_game(self, emoji: str, value: int) -> List[types.ReactionTypeEmoji]:
        if emoji not in self.games:
            return None

        if value not in self.games[emoji]:
            return None

        return [types.ReactionTypeEmoji(emoji=random.choice(self.positive_reactions))]

    async def handler(self, message: Message) -> None:
        """ 
        This handler receives messages with game
        """
        reactions = self.process_game(message.dice.emoji, message.dice.value)
        
        if reactions is not None:
            sleep(4)
            await message.react(reactions)


def register_user_handlers(dp: Dispatcher) -> None:
    PROJECT_ROOT = os.getenv("PROJECT_ROOT")
    game_handler = GameMessageHandler(config_path=PROJECT_ROOT + "/src/config.json")

    dp.message(CommandStart())(command_start_handler)
    dp.message(lambda msg: msg.dice is not None)(game_handler.handler)
