from telebot.types import CallbackQuery
from databases.databases_action import get_group_from_db, check_schedule_in_db, get_schedule_from_db, \
    add_user_last_message_in_db, check_user_last_message
from loader import bot, engine


@bot.callback_query_handler(func=lambda call: True)
def send_schedule(call: CallbackQuery):
    check_schedule_in_db(engine, call.from_user.id)

    group = get_group_from_db(engine, call.from_user.id)

    if call.data == "0":
        text = get_schedule_from_db(engine, group, 'monday')
    elif call.data == '1':
        text = get_schedule_from_db(engine, group, 'tuesday')
    elif call.data == '2':
        text = get_schedule_from_db(engine, group, 'wednesday')
    elif call.data == '3':
        text = get_schedule_from_db(engine, group, 'thursday')
    elif call.data == '4':
        text = get_schedule_from_db(engine, group, 'friday')
    elif call.data == '5':
        text = get_schedule_from_db(engine, group, 'saturday')
    elif call.data == '6':
        text = get_schedule_from_db(engine, group, 'all')

    message_id = check_user_last_message(engine, call.from_user.id)
    if message_id is not None:
        try:
            bot.edit_message_text(text, call.from_user.id, message_id, parse_mode='Markdown')
        except Exception as exe:
            print(exe)

    else:
        message_schedule = bot.send_message(call.from_user.id, text, parse_mode='Markdown')
        add_user_last_message_in_db(engine, call.from_user.id, message_schedule.message_id)

