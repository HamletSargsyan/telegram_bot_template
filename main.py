from config import bot, DEBUG, logger

def log(*args, **kwargs):
    return args, kwargs

# @error_handler
def main() -> None:
    log('Бот включён', 'info')
    logger.success('Бот включён')
    
    if DEBUG:
        log('Бот работает в режиме debug', 'warn')
        logger.warning('Бот работает в режиме debug')

    bot.infinity_polling(timeout=500, skip_pending=True)

if __name__ == "__main__":
    main()
