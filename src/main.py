import asyncio
from argparse import ArgumentParser, Namespace

from aiogram import Dispatcher
from aiogram.types import BotCommand

from config import bot, config, logger
from handlers import router
from middlewares import middlewares

dp = Dispatcher()
dp.include_router(router)


def init_middlewares():
    logger.debug("Инициализация мидлваров")  # cspell: disable-line
    for middleware in middlewares:
        dp.message.middleware(middleware())


async def init_bot_commands():
    commands = [
        BotCommand(command="start", description="start"),
    ]

    await bot.set_my_commands(commands)


async def main(args: Namespace) -> None:
    logger.info("Бот включён")

    if args.debug or config.general.debug:
        config.general.debug = True
        logger.warning("Бот работает в режиме debug")

    init_middlewares()

    await dp.start_polling(bot, handle_signals=False)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")

    args = parser.parse_args()
    asyncio.run(main(args))
