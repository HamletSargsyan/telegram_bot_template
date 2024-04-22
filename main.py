import os
import importlib

from bot import handlers  # noqa
from middlewares.register import RegisterMiddleware
from config import bot, DEBUG, logger


def import_modules():
    if not os.path.exists("./modules"):
        os.mkdir("./modules")
        os.system("touch __init__.py")

    for module in os.listdir("./modules"):
        if module.startswith("__"):
            continue
        importlib.import_module(f"modules.{module}")


def main() -> None:
    logger.info("Бот включён")

    if DEBUG:
        logger.warning("Бот работает в режиме debug")

    bot.setup_middleware(RegisterMiddleware())
    bot.infinity_polling(timeout=500, skip_pending=True)


if __name__ == "__main__":
    main()
