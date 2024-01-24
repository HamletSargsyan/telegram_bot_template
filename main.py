from bot.handlers import *

from helpers.util import error_handler, log

from config import bot, DEBUG, logger


@error_handler
def main() -> None:
    log("Бот включён", "info")
    logger.success("Бот включён")

    if DEBUG:
        log("Бот работает в режиме debug", "warn")
        logger.warning("Бот работает в режиме debug")

    bot.infinity_polling(timeout=500, skip_pending=True)


if __name__ == "__main__":
    main()
