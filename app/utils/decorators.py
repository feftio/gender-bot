from subprocess import call
import telebot.types as t
from telebot import TeleBot
from typing import Any, Callable, Optional

_bot: TeleBot = None


def init_decorators(bot: TeleBot):
    global _bot
    _bot = bot
    return bot


class BaseDecorator:
    def __init__(self, handler: Callable[[t.Message], Any]):
        self.bot = _bot
        self.handler = handler

    def __call__(self, message: t.Message):
        self.decorator(message)
        return self.handler(message)

    def decorator(self, message: t.Message):
        raise NotImplementedError('Implement %s.' % (self.__class__.__name__))


class print_message(BaseDecorator):
    def decorator(self, message):
        self.bot.reply_to(message, "Decorator worked")
