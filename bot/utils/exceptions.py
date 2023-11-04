from typing import Union

from telebot.types import Message
from config import bot


class BotException(Exception):
    stickers = {
        'no_access': 'CAACAgIAAxkBAAEmt1tlJEZj33WCGLI_w6WljslkcwUq3gACWhYAAqKeqUnmcAcRM3BgPDAE',
        'user_in_ban': 'CAACAgUAAxkBAAEm901lMUvlm00VbEpu0RGmgIpAuaksHwACPgMAAp_oJQpnBX6bh4wjRjAE',
        'in_developing': 'CAACAgIAAxkBAAEnIBdlOoMvmR7bpoR2aB7JgLkFq1Mm2QACTgIAAladvQow_mttgTIDbzAE',
        'no_arguments': 'CAACAgUAAxkBAAEmtz9lJELfRtcpKqsiXgACs0Vp9LsAAc4AAi4DAAKf6CUKFTTNuSiPpwQwBA',
        'privete_command': 'CAACAgEAAxkBAAEnIBtlOoSf6-LTajOUE9a7014FqQ2STgACoQIAAqjIIUSv4LpK6TbmKTAE'
            
    }

    def __init__(self, message: str, tg_message: Message, sticker: Union[str, None] = None):
        self.message = message
        self.tg_message = tg_message
        self.sticker = sticker

        self.__send_message()

    def __send_message(self):
        if self.sticker:
            try:
                bot.send_sticker(self.tg_message.chat.id, self.stickers[self.sticker])
            except KeyError as e:
                pass

        bot.reply_to(self.tg_message, text=self.message)



class NoAccess(BotException):
    def __init__(self, tg_message: Message):
        super().__init__("У тебя нет доступа", tg_message, sticker='no_access')

class UserIsBanned(BotException):
    def __init__(self, tg_message: Message):
        super().__init__("Ты в бане", tg_message, sticker='user_in_ban')

class InDeveloping(BotException):
    def __init__(self, tg_message: Message):
        super().__init__("В разработке", tg_message, sticker='in_developing')

class NoArguments(BotException):
    def __init__(self, tg_message: Message):
        super().__init__("Где аргументы команды??", tg_message, sticker='no_arguments')

class PriveteCommand(BotException):
    def __init__(self, tg_message: Message):
        super().__init__("Команда работает в лс", tg_message, sticker='privete_command')