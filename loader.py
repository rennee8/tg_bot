import threading
from sqlalchemy import create_engine
from telebot import TeleBot
from config_data import config

bot = TeleBot(config.BOT_TOKEN)
engine = create_engine('mysql+mysqlconnector://root:fgrgverv21%40ed@localhost:3306/tgbot_voenmeh')
lock = threading.Lock()

