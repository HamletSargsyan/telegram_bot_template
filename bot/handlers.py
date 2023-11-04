from telebot.types import Message

from .callback_query import *
from config import bot


@bot.message_handler(commands=['start'])
@error_handler
def start(message: Message) -> None:
    bot.reply_to(message, f"Hi, {message.from_user.first_name}")

