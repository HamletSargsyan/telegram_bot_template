from dataclasses import dataclass
from typing import Final, Optional

from tinylogging import (
    Logger,
    LoggingAdapterHandler,
    Level,
    BaseHandler,
    FileHandler,
)

import telebot
import toml


TELEGRAM_ID: Final = 777000


# ---------------------------------------------------------------------------- #
#                                 config types                                 #
# ---------------------------------------------------------------------------- #


@dataclass
class GeneralConfig:
    debug: bool = False


@dataclass
class DatabaseConfig:
    url: str
    name: str


@dataclass
class TelegramConfig:
    token: str
    owners: list[int]
    log_chat_id: int
    log_threat_id: Optional[int] = None


@dataclass
class Config:
    general: GeneralConfig
    database: DatabaseConfig
    telegram: TelegramConfig

    @staticmethod
    def from_file(path: str) -> "Config":
        data = toml.load(path)

        return Config(
            general=GeneralConfig(**data.get("general", {})),
            database=DatabaseConfig(**data.get("database", {})),
            telegram=TelegramConfig(**data.get("telegram", {})),
        )


config: Final = Config.from_file("config.toml")

# ---------------------------------------------------------------------------- #

bot = telebot.TeleBot(
    config.telegram.token,
    parse_mode="html",
    skip_pending=True,
    num_threads=10,
    disable_web_page_preview=True,
    use_class_middlewares=True,
)


class TelegramLogsHandler(BaseHandler):
    def emit(self, record):
        from helpers.utils import log

        self.formatter.colorize = False

        log_entry = self.formatter.format(record)
        log(log_entry, record)


logger: Final[Logger] = Logger("Bot", level=Level.INFO)
logger.handlers.add(TelegramLogsHandler())
logger.handlers.add(FileHandler("bot.log"))


telebot.logger.handlers = []
for handler in logger.handlers:
    telebot.logger.addHandler(LoggingAdapterHandler(handler))
telebot.logger.setLevel("INFO")
