import datetime
from telebot.types import Message
from loader import bot, engine
from databases.databases_action import add_user_last_message_in_db


@bot.message_handler(commands=["which_week"])
def which_week(message: Message):
    add_user_last_message_in_db(engine, message.from_user.id)
    # Получаем текущую дату
    current_date = datetime.date.today()
    # Получаем номер недели
    week_number = current_date.isocalendar()[1]
    # Проверяем, четная или нечетная неделя
    a = week_number % 2 != 0

    if not a:
        bot.send_message(message.from_user.id, 'Сегодня нечетная неделя')
    else:
        bot.send_message(message.from_user.id, 'Сегодня четная неделя')
