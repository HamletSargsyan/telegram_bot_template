from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Final, Optional

from tinylogging import (
    Logger,
    LoggingAdapterHandler,
    Level,
    BaseHandler,
    FileHandler,
)

import telebot
from telebot.util import antiflood, escape, split_string

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


logger: Final = Logger("Bot", level=Level.INFO)


class TelegramLogsHandler(BaseHandler):
    def emit(self, record):
        emoji_dict = {
            Level.DEBUG: "👾",
            Level.INFO: "ℹ️",
            Level.WARNING: "⚠️",
            Level.ERROR: "🛑",
            Level.CRITICAL: "⛔",
        }
        current_time = datetime.now(UTC).strftime("%d.%m.%Y %H:%M:%S")
        log_template = (
            f'<b>{emoji_dict.get(record.level, "")} {record.level}</b>\n\n'
            f"{current_time}\n\n"
            f"<b>Логгер:</b> <code>{record.name}</code>\n"  # cspell: disable-line
            # f"<b>Модуль:</b> <code>{record.module}</code>\n"
            # f"<b>Путь к файлу:</b> <code>{record.pathname}</code>\n"
            # f"<b>Файл</b>: <code>{record.filename}</code>\n"
            # f"<b>Строка:</b> {record.lineno}\n\n"
            '<pre><code class="language-shell">{text}</code></pre>'
        )

        for text in split_string(record.message, 3000):
            try:
                antiflood(
                    bot.send_message,
                    config.telegram.log_chat_id,
                    log_template.format(text=escape(text)),
                    message_thread_id=config.telegram.log_threat_id,
                )
            except Exception as e:
                logger.critical(str(e))
                logger.log(text, record.level)


logger.handlers.add(TelegramLogsHandler())
logger.handlers.add(FileHandler("bot.log"))


telebot.logger.handlers = []
for handler in logger.handlers:
    telebot.logger.addHandler(LoggingAdapterHandler(handler))
telebot.logger.setLevel("INFO")
