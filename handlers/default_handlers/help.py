from telebot.types import Message
from config_data.config import DEFAULT_COMMANDS
from loader import bot, engine
from databases.databases_action import add_user_last_message_in_db


@bot.message_handler(commands=["help"])
def bot_help(message: Message):
    add_user_last_message_in_db(engine, message.from_user.id)
    text = [f"/{command} - {desk}" for command, desk in DEFAULT_COMMANDS]
    bot.send_message(message.from_user.id, "\n".join(text))
