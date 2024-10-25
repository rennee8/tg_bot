from tinydb import TinyDB
from datetime import datetime
from telebot.types import Message, CallbackQuery
from loader import lock
from utils.misc.request_for_site import get_group_list, get_schedule, start_browser


def check_groups_db():
    try:
        with lock:

            db = TinyDB(r'databases\groups.json', ensure_ascii=False, encoding='utf-8')
            current_date = datetime.now()
            create_date = db.get(doc_id=2)
            if not create_date:
                browser = start_browser()
                group_dict = get_group_list(browser)
                db.insert({'groups': group_dict})
                db.insert({'create_date': str(current_date.date())})
                return
            elif (current_date - datetime.strptime(create_date['create_date'], '%Y-%m-%d')).days >= 3:

                browser = start_browser()
                group_dict = get_group_list(browser)
                for table_name in db.tables():
                    db.table(table_name).truncate()
                db.insert({'groups': group_dict})
                db.insert({'create_date': str(current_date.date())})
                return
            else:
                return
    finally:
        db.close()


def get_group_list_from_db(type_return):
    try:
        db = TinyDB(r'databases\groups.json', ensure_ascii=False, encoding='utf-8')
        group_dict = db.get(doc_id=1)['groups']
        text_groups = ''
        list_groups = []
        for group in group_dict:
            text_groups += group + '\n'
            list_groups.append(group)
        if type_return == 'str':
            return text_groups
        elif type_return == 'list':
            return list_groups
        else:
            return
    finally:
        db.close()


def get_value_group_from_db(group_user: str) -> str:
    try:
        db = TinyDB(r'databases\groups.json', ensure_ascii=False, encoding='utf-8')
        group_dict = db.get(doc_id=1)['groups']
        for group, value in group_dict.items():
            if group_user == group:
                return value
    finally:
        db.close()


def check_user_db(message: Message) -> bool:
    try:
        db = TinyDB(r'databases\users.json', ensure_ascii=False, encoding='utf-8')
        id_dict = db.get(doc_id=1)
        if not id_dict:
            return False

        user_dict = id_dict['users']
        for user_id in user_dict:
            if message.from_user.id == int(user_id):
                return True
        else:
            return False
    finally:
        db.close()


def add_user_in_db(message: Message):
    try:
        db = TinyDB(r'databases\users.json', ensure_ascii=False, encoding='utf-8')

        new_user = {message.from_user.id: {'group': message.text.upper(), 'user_name': message.from_user.username}}

        id_dict = db.get(doc_id=1)
        if not id_dict:
            user = {"users": new_user}
            db.insert(user)

        else:
            db.update({"users": {**db.get(doc_id=1)["users"], **new_user}}, doc_ids=[1])
    finally:
        db.close()


def delete_user_in_db(message: Message):
    try:
        db = TinyDB(r'databases\users.json', ensure_ascii=False, encoding='utf-8')
        doc = db.get(doc_id=1)
        users = doc['users']
        users.pop(str(message.from_user.id), None)  # None предотвращает ошибку, если пользователя нет
        db.update({"users": users}, doc_ids=[1])
    finally:
        db.close()


def get_group_from_db(user_id: str) -> str:
    try:
        db = TinyDB(r'databases\users.json', ensure_ascii=False, encoding='utf-8')
        group = db.get(doc_id=1)['users'][user_id]['group']
        # for user, group in group_dict.items():
        #     if user == user_id:
        #         return group
        return group
    finally:
        db.close()


def check_schedule_in_db(call: CallbackQuery):
    try:
        db = TinyDB(r'databases\schedule.json', ensure_ascii=False, encoding='utf-8')
        current_date = datetime.now()
        create_date = db.get(doc_id=1)
        group = get_group_from_db(str(call.from_user.id))

        if not create_date:
            return False

        group_dict = create_date['groups']

        for group in group_dict:
            if get_group_from_db(str(call.from_user.id)) == group:
                if (current_date - datetime.strptime(create_date['groups'][group]['create_date'],
                                                     '%Y-%m-%d')).days >= 3:
                    return False
                else:
                    return True
        else:
            return False
    finally:
        db.close()


def add_schedule_in_db(call: CallbackQuery):
    try:
        current_date = datetime.now()
        db = TinyDB(r'databases\schedule.json', ensure_ascii=False, encoding='utf-8')
        group = get_group_from_db(str(call.from_user.id))
        value_group = get_value_group_from_db(group)
        browser = start_browser()
        schedule_dict = get_schedule(browser, value_group)

        format_schedule_dict = {}
        for key, value in schedule_dict.items():
            text_list = value.split('\n')
            day = text_list[0]

            # Словарь для хранения группировок по времени
            schedule = {}

            # Проходим по оставшимся строкам и группируем по времени
            for line in text_list[2:]:  # Пропускаем первые две строки
                time = line.split(' ')[0]  # Получаем время (первая часть строки)
                if time not in schedule:
                    schedule[time] = []
                schedule[time].append(line)

            # Формируем итоговую строку
            output = [day, '—' * 21]

            for time, entries in schedule.items():
                for entry in entries:
                    if 'нечетная' in entry.lower():  # Проверка на "нечетная"
                        output.append(f'_{entry}_')  # Жирный текст
                    else:
                        output.append(f'`{entry}`')  # Моноширинный текст
                output.append('—' * 21)  # Добавляем разделитель

            # Присоединяем все части и выводим результат
            final_text = '\n'.join(output)

            format_schedule_dict[key] = final_text

        new_group = {group: {'schedule': format_schedule_dict, 'create_date': str(current_date.date())}}

        id_dict = db.get(doc_id=1)
        if not id_dict:
            db.insert({'groups': new_group})
        else:
            db.update({"groups": {**db.get(doc_id=1)["groups"], **new_group}}, doc_ids=[1])
    finally:
        db.close()


def get_schedule_from_db(group, day) -> str:
    try:
        db = TinyDB(r'databases\schedule.json', ensure_ascii=False, encoding='utf-8')
        schedule = db.get(doc_id=1)['groups'][group]['schedule']

        if day == 'all':
            text = f'Группа {group}\n\n'
            for _, day_schedule in schedule.items():
                text += day_schedule + '\n\n'
            return text
        else:
            for day_id, day_schedule in schedule.items():
                if day == day_id:
                    return f'Группа {group}\n\n' + day_schedule
            else:
                return "Пар нет"
    finally:
        db.close()


def add_user_last_message_in_db(user_id: str, last_message: str):
    try:
        db = TinyDB(r'databases\users_last_message.json', ensure_ascii=False, encoding='utf-8')
        new_data = {user_id: last_message}
        id_dict = db.get(doc_id=1)

        if not id_dict:
            user = {"users": new_data}
            db.insert(user)

        else:
            db.update({"users": {**db.get(doc_id=1)["users"], **new_data}}, doc_ids=[1])
    finally:
        db.close()


def check_user_last_message(user_id: str) -> str:
    try:
        db = TinyDB(r'databases\users_last_message.json', ensure_ascii=False, encoding='utf-8')
        id_dict = db.get(doc_id=1)
        if not id_dict:
            return 'none'
        message_id = id_dict['users'][user_id]
        return message_id
    finally:
        db.close()


def get_last_message_id(user_id: str) -> int:
    try:
        db = TinyDB(r'databases\users_last_message.json', ensure_ascii=False, encoding='utf-8')
        last_message_id = db.get(doc_id=1)['users'][user_id]
        return int(last_message_id)
    finally:
        db.close()
