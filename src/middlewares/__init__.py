from typing import Type
from telebot.handler_backends import BaseMiddleware

from .register import RegisterMiddleware


middlewares: list[Type[BaseMiddleware]] = [
    RegisterMiddleware,
]

__all__ = ["middlewares"]
