import re
from typing import Any, Union
import traceback
from telebot.types import Message

from .logging import log, console_log

def check_username(username: str):
    pattern = r'^@[A-Za-z0-9_]{5,32}$'

    if re.match(pattern, username):
        return True
    else:
        return False


ban_users_list = []


def error_handler(func) -> Union[None, Any]:
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            error_traceback = traceback.format_exc()
            log(f'Произошла ошибка: {str(e)}\n{__file__}\n\n{error_traceback}', 'error')
            console_log(f"Произошла ошибка: {str(e)}\n{__file__}", 'error')
            print(traceback.format_exc())
    return wrapper


@error_handler
def ban_check(message: Message) -> bool:
    user_id = message.from_user.id

    if user_id in ban_users_list:
        from .exceptions import UserIsBanned
        UserIsBanned(message)
        return True
    return False


class ReprMixin:
    def __repr__(self):
        class_name = self.__class__.__name__
        attributes = "\n".join([f"  {key}: {value!r}" for key, value in self.__dict__.items()])
        return f"{class_name}:\n\t\t{attributes}"
