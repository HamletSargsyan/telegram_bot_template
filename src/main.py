from handlers import message  # noqa
from middlewares import middlewares
from config import bot, config, logger


def main() -> None:
    logger.info("Бот включён")

    if config.general.debug:
        logger.warning("Бот работает в режиме debug")

    for middleware in middlewares:
        bot.setup_middleware(middleware())
    bot.infinity_polling(timeout=500, skip_pending=True)


if __name__ == "__main__":
    main()
