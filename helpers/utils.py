from typing import Union, Literal
from datetime import datetime

from telebot.util import antiflood, escape, smart_split

from config import bot, logger, timezone, log_chat_id, log_thread_id


def error_handler(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.exception(e)
            log(str(e), "error")

    return wrapper


@error_handler
def log(
    message: str,
    level: Union[
        Literal["error"], Literal["warn"], Literal["info"], Literal["success"]
    ],
):
    emoji_dict = {"error": "🛑", "warn": "⚠️", "info": "ℹ️", "success": "✅"}

    time = datetime.now(timezone)
    level_ = f"{emoji_dict.get(level)} {level.upper()}"

    try:
        for mess in smart_split(escape(message)):
            template = (
                f"{level_}\n\n"
                f"{time}\n\n"
                f"<pre><code class='language-shell'>{mess}</code></pre>"
            )
            antiflood(
                bot.send_message, log_chat_id, template, message_thread_id=log_thread_id
            )
    except Exception as e:
        logger.exception(e)
