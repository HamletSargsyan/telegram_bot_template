from telebot.types import CallbackQuery
from .utils.utils import error_handler

from config import bot

@bot.callback_query_handler(func=lambda call: True)
@error_handler
def callback_query_handler(call: CallbackQuery) -> None:
    ...