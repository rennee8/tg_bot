import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit("Переменные окружения не загружены, т.к. отсутсвует файл .env")
else:
    load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
DEFAULT_COMMANDS = (
    ('start', 'Запустить бота'),
    ('help', 'Вывести справку'),
    ('groups', 'Вывести список всех групп'),
    ('set_group', 'Изменить свою группу'),
    ('which_week', 'Какая сегодня неделя?'),
)
