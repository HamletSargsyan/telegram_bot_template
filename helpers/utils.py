from typing import Union, Litera
from datetime import datetime

from telebot.util import antifloot, escape, smart_split

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
    level: Union[Literal["error"], Literal["warn"], Literal["log"], Literal["success"]],
):
    ...
