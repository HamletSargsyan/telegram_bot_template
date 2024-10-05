import logging
from dataclasses import dataclass
from typing import Final, Optional

from tinylogging import Logger, LoggingAdapterHandler, Level, BaseHandler

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

        log_entry = self.formatter.format(record)
        log(log_entry, record.level.name, record)  # type: ignore # TODO


logger: Final[Logger] = Logger("Bot", level=Level.INFO)
logger.handlers.add(TelegramLogsHandler())

formatter = logging.Formatter(
    '%(asctime)s (%(filename)s:%(lineno)d %(threadName)s) %(levelname)s - %(name)s: "%(message)s"'  # cspell: disable-line
)


telebot.logger.addHandler(LoggingAdapterHandler(TelegramLogsHandler()))
telebot.logger.setLevel("INFO")
