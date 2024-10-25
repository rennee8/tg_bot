from telebot.types import Message

from handlers.default_handlers.which_week import which_week
from handlers.default_handlers.groups import get_groups
from handlers.default_handlers.help import bot_help
from databases.databases_action_old import check_groups_db, check_user_db, get_group_list_from_db, add_user_in_db, delete_user_in_db, add_user_last_message_in_db
from keyboards.inline.day_tittle import day_tittle
from loader import bot


@bot.message_handler(commands=["start"])
def bot_start(message: Message):
    add_user_last_message_in_db(str(message.from_user.id), 'none')
    check_groups_db()

    user = check_user_db(message)
    # Если юзер уже писал и указывал группу то берем из базы его группу
    if not user:
        bot.send_message(message.from_user.id, f"Привет, введи свою группу.\nДля просмотра команд введи /help")
        bot.register_next_step_handler(message, input_group, False)

    else:
        keyboard = day_tittle()
        bot.send_message(message.chat.id, "Какой день недели ты хочешь выбрать?", reply_markup=keyboard)

@bot.message_handler(commands=["set_group"])
def bot_set_group(message: Message):
    add_user_last_message_in_db(str(message.from_user.id), 'none')
    if check_user_db(message):

        bot.send_message(message.from_user.id, 'Введи группу')
        bot.register_next_step_handler(message, input_group, True)
    else:
        bot.send_message(message.from_user.id, 'Ты ни разу не вводил группу, поэтому сообщи ее мне')
        bot.register_next_step_handler(message, input_group, False)
    pass



def input_group(message: Message, delete):
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


    # Если группа есть в базе данных то кидаем выбор какую ненделю выбрать если нет, то пишем такой группы нет, возможно вы имели ввиду такую то такуюто
    if message.text.upper() in get_group_list_from_db('list'):
        if delete:
            delete_user_in_db(message)

        else:
            bot.send_message(745543822, f'Добавлен новый юзер. Ник: @{message.from_user.username}')

        user = check_user_db(message)

        if not user:

            add_user_in_db(message, bot)
        keyboard = day_tittle()
        bot.send_message(message.chat.id, "Какой день недели ты хочешь выбрать?", reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, "Такой группы нет(")
        bot.register_next_step_handler(message, input_group, False)
