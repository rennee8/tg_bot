from telebot.types import Message
from databases.databases_action import check_user_db, get_group_list_from_db, check_groups_db, add_user_in_db, \
    add_user_last_message_in_db
from handlers.default_handlers.which_week import which_week
from handlers.default_handlers.groups import get_groups
from handlers.default_handlers.help import bot_help
from keyboards.inline.day_tittle import day_tittle
from loader import bot, engine


@bot.message_handler(commands=["start"])
def bot_start(message: Message):
    add_user_last_message_in_db(engine, message.from_user.id)
    check_groups_db(engine)

    user = check_user_db(engine, message.from_user.id)
    if not user:
        bot.send_message(message.from_user.id, f"Привет, введи свою группу.\nДля просмотра команд введи /help")
        bot.register_next_step_handler(message, input_group)

    else:
        keyboard = day_tittle()
        bot.send_message(message.chat.id, "Какой день недели ты хочешь выбрать?", reply_markup=keyboard)


@bot.message_handler(commands=["set_group"])
def bot_set_group(message: Message):
    add_user_last_message_in_db(engine, message.from_user.id)
    if check_user_db(engine, message.from_user.id):

        bot.send_message(message.from_user.id, 'Введи группу')
        bot.register_next_step_handler(message, input_group, True)
    else:
        bot.send_message(message.from_user.id, 'Ты ни разу не вводил группу, поэтому сообщи ее мне')
        bot.register_next_step_handler(message, input_group)
    pass


def input_group(message: Message, update: bool = False):
    if message.text == '/start':
        bot_start(message)
        return
    elif message.text == '/help':
        bot_help(message)
        return
    elif message.text == '/groups':
        get_groups(message)
        return
    elif message.text == '/set_group':
        bot_set_group(message)
        return
    elif message.text == '/which_week':
        which_week(message)
        return

    if message.text.upper() in get_group_list_from_db(engine, 'list'):
        if update:
            add_user_in_db(engine, message)

        else:
            bot.send_message(745543822, f'Добавлен новый юзер. Ник: @{message.from_user.username}')

        user = check_user_db(engine, message.from_user.id)

        if not user:
            add_user_in_db(engine, message)
        keyboard = day_tittle()
        bot.send_message(message.chat.id, "Какой день недели ты хочешь выбрать?", reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, "Такой группы нет(")
        bot.register_next_step_handler(message, input_group)
