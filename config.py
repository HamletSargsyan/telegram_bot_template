import os
from dotenv import load_dotenv
import pytz
import telebot

load_dotenv()

DEBUG = True

TOKEN = os.getenv('BOT_TOKEN')
DB_URL = os.getenv('DB_URL')

bot = telebot.TeleBot(TOKEN, parse_mode='html')

admin_chat_id = ''

log_chat_id = ''
log_message_thread_id = 0

timezone = pytz.timezone('Europe/Moscow')
