import threading
from sqlalchemy import create_engine
from telebot import TeleBot
from config_data import config

bot = TeleBot(config.BOT_TOKEN)
engine = create_engine(f'mysql+pymysql://{config.USER_BD}:{config.PASSWORD_DB}@{config.HOST_PORT}/{config.DB_NAME}')
lock = threading.Lock()

