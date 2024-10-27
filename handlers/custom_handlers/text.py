from databases.databases_action import add_user_last_message_in_db
from loader import bot, engine
from telebot.types import Message


@bot.message_handler(func=lambda message: not message.text.startswith('/'), content_types=['text'])
def answer_for_text(message: Message):
    add_user_last_message_in_db(engine, message.from_user.id)
    bot.send_message(message.from_user.id, 'Я не понимаю выбери команду!')
