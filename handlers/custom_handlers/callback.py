from telebot.types import CallbackQuery
from loader import bot
from databases.databases_action_old import check_schedule_in_db, add_schedule_in_db, get_schedule_from_db, get_group_from_db, \
    add_user_last_message_in_db, check_user_last_message, get_last_message_id


@bot.callback_query_handler(func=lambda call: True)
def send_schedule(call: CallbackQuery):
    if not check_schedule_in_db(call):
        add_schedule_in_db(call)

    group = get_group_from_db(str(call.from_user.id))

    if call.data == "0":
        text = get_schedule_from_db(group, 'понедельник')
    elif call.data == '1':
        text = get_schedule_from_db(group, 'вторник')
    elif call.data == '2':
        text = get_schedule_from_db(group, 'среда')
    elif call.data == '3':
        text = get_schedule_from_db(group, 'четверг')
    elif call.data == '4':
        text = get_schedule_from_db(group, 'пятница')
    elif call.data == '5':
        text = get_schedule_from_db(group, 'суббота')
    elif call.data == '6':
        text = get_schedule_from_db(group, 'all')
    if check_user_last_message(str(call.from_user.id)) != 'none':
        try:
            bot.edit_message_text(text, call.from_user.id, get_last_message_id(str(call.from_user.id)), parse_mode='Markdown')
        except Exception:
            pass

    else:
        message_schedule = bot.send_message(call.from_user.id, text, parse_mode='Markdown')
        add_user_last_message_in_db(str(call.from_user.id), str(message_schedule.message_id))

