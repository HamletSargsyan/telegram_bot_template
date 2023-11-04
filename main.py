from bot import rassilka
from bot.handlers import *
from bot.utils.logging import console_log, log
from config import bot, DEBUG


@error_handler
def main() -> None:
    log('Бот включён', 'info')
    console_log('Бот включён', 'success')
    
    if DEBUG:
        log('Бот работает в режиме debug', 'warn')
        console_log('Бот работает в режиме debug', 'warn')

    bot.infinity_polling(timeout=500, skip_pending=True)

if __name__ == "__main__":
    main()
