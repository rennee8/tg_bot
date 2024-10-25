from telebot.types import Message
from loader import bot
from databases.databases_action_old import check_groups_db, get_group_list_from_db, add_user_last_message_in_db


@bot.message_handler(commands=["groups"])
def get_groups(message: Message):
    add_user_last_message_in_db(str(message.from_user.id), 'none')
    check_groups_db()

    text_groups = get_group_list_from_db('str')
    bot.send_message(message.from_user.id,f"Список всех групп:\n{text_groups}")

