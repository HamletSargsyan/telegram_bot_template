import os
from dotenv import load_dotenv
import pytz
import telebot
from loguru import logger

load_dotenv()

DEBUG = True

TOKEN = os.getenv("BOT_TOKEN")
DB_URL = os.getenv("DB_URL")

if not TOKEN:
    raise ValueError
elif not DB_URL:
    raise ValueError

bot = telebot.TeleBot(TOKEN, parse_mode="html")

log_chat_id = ""
log_thread_id = 0

timezone = pytz.timezone("Europe/Moscow")

logger.add("bot_logs.log", rotation="1 week")
