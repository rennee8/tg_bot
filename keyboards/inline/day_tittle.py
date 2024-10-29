from telebot.types import Message, InlineKeyboardButton
from telebot import types


def day_tittle():
    keyboard = types.InlineKeyboardMarkup(row_width=6)
    days_list = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Вся неделя']
    keyboard.add(InlineKeyboardButton(text='Понедельник', callback_data='0'), InlineKeyboardButton(text='Вторник', callback_data='1'), InlineKeyboardButton(text='Среда', callback_data='2'))
    keyboard.add(InlineKeyboardButton(text='Четверг', callback_data='3'), InlineKeyboardButton(text='Пятница', callback_data='4'), InlineKeyboardButton(text='Суббота', callback_data='5'))
    keyboard.add(InlineKeyboardButton(text='Вся неделя', callback_data='6'))

    return keyboard
