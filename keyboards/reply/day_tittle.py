from telebot.types import Message
from telebot.types import KeyboardButton, ReplyKeyboardMarkup


def day_tittle():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    days_list = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Вся неделя']

    keyboard.add(KeyboardButton('Понедельник'), KeyboardButton('Вторник'), KeyboardButton('Среда'))
    keyboard.add(KeyboardButton('Четверг'), KeyboardButton('Пятница'), KeyboardButton('Пятница'))
    keyboard.add(KeyboardButton('Вся неделя'))

    return keyboard
