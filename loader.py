import threading
from sqlalchemy import create_engine
from telebot import TeleBot
from config_data import config

bot = TeleBot(config.BOT_TOKEN)
engine = create_engine('mysql+pymysql://root:Qwerty12345@localhost:3306/tg_bot')
lock = threading.Lock()

