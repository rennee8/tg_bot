import threading
from sqlalchemy import create_engine
from telebot import TeleBot
from config_data import config

bot = TeleBot(config.BOT_TOKEN)
engine = create_engine(f'mysql+pymysql://{config.USER_BD}:{config.PASSWORD_BD}@localhost:3306/tg_bot')
lock = threading.Lock()

