import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit("Переменные окружения не загружены, т.к. отсутсвует файл .env")
else:
    load_dotenv()

ENABLE_TIMING = True
BOT_TOKEN = os.getenv("BOT_TOKEN")
USER_BD = os.getenv("USER_BD")
PASSWORD_DB = os.getenv("PASSWORD_DB")
HOST_PORT = os.getenv("HOST_PORT")
DB_NAME = os.getenv("DB_NAME")

DEFAULT_COMMANDS = (
    ('start', 'Запустить бота'),
    ('help', 'Вывести справку'),
    ('groups', 'Вывести список всех групп'),
    ('set_group', 'Изменить свою группу'),
    ('which_week', 'Какая сегодня неделя?'),
)
