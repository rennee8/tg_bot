from telebot.types import Message
from databases.databases_action import add_user_last_message_in_db
from loader import bot, engine
from databases.databases_action import check_groups_db, get_group_list_from_db


@bot.message_handler(commands=["groups"])
def get_groups(message: Message):
    add_user_last_message_in_db(engine, message.from_user.id)
    check_groups_db(engine)

    text_groups = get_group_list_from_db(engine, 'str')
    bot.send_message(message.from_user.id,f"Список всех групп:\n{text_groups}")

