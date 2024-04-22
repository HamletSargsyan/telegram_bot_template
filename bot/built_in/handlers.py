import time
from telebot.types import Message
from telebot.util import antiflood

from database.funcs import database
from scripts.install_module import installer

from config import bot, bot_owners


_messages = {}


def _update_message(message: Message, text: str):
    if message.id not in _messages:
        _messages[message.id] = message.text
    mess = _messages[message.id]

    text = f"<blockquote>{mess}\n{text}</blockquote>"
    antiflood(bot.edit_message_text, text, message.chat.id, message.id)
    _messages[message.id] = text


@bot.message_handler(commands=["ext"])
def ext_cmd(message: Message):
    user = database.users.get(id=message.from_user.id)

    if user.id not in bot_owners:
        return

    args = str(message.text).split(" ")
    if len(args) == 1:
        return

    msg = bot.reply_to(message, "<blockquote>Обработка...</blockquote>")
    time.sleep(1)
    match args[1]:
        case "list":
            result = installer.list()
            if isinstance(result, list):
                mess = f"Всего модулей найдено: {len(result)}\n\n"
                mess += "\n".join(result)
            else:
                mess = result
            _update_message(msg, f"{mess}")
        case "install":
            _update_message(msg, f"Установка модуля {args[2]}")
            result = installer.install(args[2])
            _update_message(msg, f"{result}")
        case "update":
            _update_message(msg, f"Обновление модуля {args[2]}")
            result = installer.update(args[2])
            _update_message(msg, f"{result}")
        case "remove":
            _update_message(msg, f"Удаление модуля {args[2]}")
            result = installer.remove(args[2])
            _update_message(msg, f"{result}")
