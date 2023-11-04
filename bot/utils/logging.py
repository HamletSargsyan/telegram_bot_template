from rich import print
from datetime import datetime
from telebot.util import smart_split, escape, antiflood

from config import (log_chat_id, log_message_thread_id, bot, timezone)

def log(log_text, log_level: str = 'info') -> None:
    """
    Sends a log message to the log chat.

    Args:
        log_text (str): The text to be logged.
        log_level (str): The logging level. Defaults to '`info`'.
            Allowed values: '`info`', '`warn`', '`error`'.
    """
    emoji_dict = {
        'info': 'ℹ️',
        'warn': '⚠️',
        'error': '🛑'
    }
    current_time = datetime.now(timezone).strftime('%d.%m.%Y %H:%M:%S')
    log_template = f'<b>{emoji_dict.get(log_level, "ℹ️")} {log_level.upper()}</b>\n\n' \
                   f'{current_time}\n\n' \
                   f'{escape(str(log_text))}'
    
    disable_notification = True if log_level == 'error' else False

    try:
        msg = antiflood(bot.send_message, log_chat_id, smart_split(log_template), message_thread_id=log_message_thread_id, disable_web_page_preview=True, disable_notification=disable_notification)
    except Exception as e:
        msg = antiflood(bot.send_message, log_chat_id, smart_split(log_template), message_thread_id=log_message_thread_id, disable_web_page_preview=True, disable_notification=disable_notification)
        print(log_template)


    
def console_log(message: str, level: str = 'log') -> None:
    level_colors = {
        'success': 'bright_green',
        'warn': 'bright_yellow',
        'error': 'bright_red',
        'log': 'bright_blue'
    }

    template = "[[{level_color}]{level}[/{level_color}]] | [bright_white]{time} | {message}[/bright_white]"
    current_time = datetime.now(timezone).strftime('%H:%M:%S %d.%m.%Y')

    text = template.format(level_color=level_colors[level],
                                    level=level,
                                    time=current_time,
                                    message=str(message))
    
    print(text)

