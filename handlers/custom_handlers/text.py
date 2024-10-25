from loader import bot
from telebot.types import Message
from databases.databases_action_old import add_user_last_message_in_db


@bot.message_handler(func=lambda message: not message.text.startswith('/'), content_types=['text'])
def answer_for_text(message: Message):
    add_user_last_message_in_db(str(message.from_user.id), 'none')
    bot.send_message(message.from_user.id, 'Я не понимаю выбери команду!')
