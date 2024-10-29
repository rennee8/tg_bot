from datetime import datetime
from typing import Any
from sqlalchemy import update
from sqlalchemy.orm import sessionmaker
from telebot.types import Message
from databases.tables import Groups, Update_Table_Date, Users, Schedule, Users_Last_Message
from loader import lock
from utils.converter import convert_schedule
from utils.decorators import timeit, timer_databases
from utils.request_for_site import start_browser, get_group_list, get_schedule

@timeit
def check_groups_db(engine) -> None:
    with lock:
        with sessionmaker(bind=engine)() as session:

            if session.query(Groups).first() is None:
                browser = start_browser()
                group_dict = get_group_list(browser)
                for group, value_group in group_dict.items():
                    new_user = Groups(group=group, value_group=int(value_group))
                    session.add(new_user)
                exists = session.query(Update_Table_Date).filter(
                    Update_Table_Date.table_name == Groups.__tablename__).first() is not None

                if exists:
                    stmt = update(Update_Table_Date).where(Update_Table_Date.table_name == Groups.__tablename__)
                    session.execute(stmt)
                else:
                    session.add(Update_Table_Date(table_name=Groups.__tablename__))

                session.commit()
            elif (datetime.now() - session.query(Update_Table_Date).filter(
                    Update_Table_Date.table_name == 'groups').first().created_at).days >= 3:
                session.query(Groups).delete()
                browser = start_browser()
                group_dict = get_group_list(browser)
                for group, value_group in group_dict.items():
                    new_user = Groups(group=group, value_group=int(value_group))
                    session.add(new_user)

                stmt = update(Update_Table_Date).where(Update_Table_Date.table_name == Groups.__tablename__)
                session.execute(stmt)
                session.commit()


@timeit
def get_group_list_from_db(engine, type_return: str) -> Any:
    with sessionmaker(bind=engine)() as session:
        group_values = session.query(Groups.group).all()
        if type_return == 'str':
            text_groups = ''
            for group in group_values:
                text_groups += group[0] + '\n'
            return text_groups
        elif type_return == 'list':
            list_groups = [group[0] for group in group_values]
            return list_groups


@timeit
def get_value_group_from_db(engine, group_user: str) -> str:
    with sessionmaker(bind=engine)() as session:
        group_record = session.get(Groups, group_user)
        return str(group_record.value_group)


@timeit
def get_all_values_group_form_db(engine) -> list:
    with sessionmaker(bind=engine)() as session:
        values = session.query(Groups.group, Groups.value_group).all()
        values_list = [value for value in values]
        return values_list

@timer_databases
@timeit
def check_user_db(engine, user_id: int) -> bool:
    with sessionmaker(bind=engine)() as session:
        user_record = session.get(Users, user_id)
        if user_record is None:
            return False
        else:
            return True


@timeit
def add_user_in_db(engine, message: Message):
    with sessionmaker(bind=engine)() as session:
        user_exist = session.get(Users, message.from_user.id)
        if user_exist:
            session.query(Users).filter(Users.id == message.from_user.id).update({"group": message.text.upper()})
        else:
            new_user = Users(id=message.from_user.id, user_name=message.from_user.username, group=message.text.upper())

            session.add(new_user)
        session.commit()

@timer_databases
@timeit
def get_group_from_db(engine, user_id: int) -> str:
    with sessionmaker(bind=engine)() as session:
        group_record = session.get(Users, user_id)
        return str(group_record.group)


@timeit
def check_schedule_in_db(engine, user_id: int) -> None:
    with sessionmaker(bind=engine)() as session:
        group = session.get(Users, user_id).group
        schedule_record = session.get(Schedule, group)

        if not schedule_record:
            add_schedule_in_db(engine, 'add', user_id)

        elif (datetime.now() - schedule_record.created_at).days >= 3:
            add_schedule_in_db(engine, 'update', user_id)


@timeit
def add_schedule_in_db(engine, type_act: str, user_id: int = None, group: str = None,
                       schedule_dict: dict = None) -> None:
    with sessionmaker(bind=engine)() as session:
        if group is None:
            group = session.get(Users, user_id).group

        value_group = str(session.get(Groups, group).value_group)

        if schedule_dict is None:
            browser = start_browser()
            schedule_dict = get_schedule(browser, value_group)

        convert_schedule_dict = convert_schedule(schedule_dict)
        if type_act == 'update':
            for key, schedule in convert_schedule_dict.items():
                if key == 'понедельник':
                    session.query(Schedule).filter(Schedule.group == group).update({"monday": schedule})
                    continue
                elif key == 'вторник':
                    session.query(Schedule).filter(Schedule.group == group).update({"tuesday": schedule})
                    continue
                elif key == 'среда':
                    session.query(Schedule).filter(Schedule.group == group).update({"wednesday": schedule})
                    continue
                elif key == 'четверг':
                    session.query(Schedule).filter(Schedule.group == group).update({"thursday": schedule})
                    continue
                elif key == 'пятница':
                    session.query(Schedule).filter(Schedule.group == group).update({"friday": schedule})
                    continue
                elif key == 'суббота':
                    session.query(Schedule).filter(Schedule.group == group).update({"saturday": schedule})
                    continue
        elif type_act == 'add':
            session.add(Schedule(group=group,
                                 monday=convert_schedule_dict.get('понедельник'),
                                 tuesday=convert_schedule_dict.get('вторник'),
                                 wednesday=convert_schedule_dict.get('среда'),
                                 thursday=convert_schedule_dict.get('четверг'),
                                 friday=convert_schedule_dict.get('пятница'),
                                 saturday=convert_schedule_dict.get('суббота'),
                                 )
                        )
        session.commit()


@timeit
def get_schedule_from_db(engine, group: str, day: str) -> str:
    with sessionmaker(bind=engine)() as session:
        schedule_record = session.get(Schedule, group)
        if day == 'all':
            text = f'Группа {group}\n\n' + \
                   (str(schedule_record.monday) if schedule_record.monday is not None else '') + '\n\n' + \
                   (str(schedule_record.tuesday) if schedule_record.tuesday is not None else '') + '\n\n' + \
                   (str(schedule_record.friday) if schedule_record.friday is not None else '') + '\n\n' + \
                   (str(schedule_record.thursday) if schedule_record.thursday is not None else '') + '\n\n' + \
                   (str(schedule_record.friday) if schedule_record.friday is not None else '') + '\n\n' + \
                   (str(schedule_record.saturday) if schedule_record.saturday is not None else '')
            return text
        else:
            text = getattr(schedule_record, day)
            if text is None:
                return 'Пар нет'
            else:
                return f'Группа {group}\n\n' + text


@timeit
def add_user_last_message_in_db(engine, user_id: int, last_message_id: int = None):
    with sessionmaker(bind=engine)() as session:
        user_lm_record = session.get(Users_Last_Message, user_id)
        if user_lm_record:
            session.query(Users_Last_Message).filter(Users_Last_Message.id == user_id).update(
                {"message_id": last_message_id})
        else:

            session.add(Users_Last_Message(id=user_id, message_id=last_message_id))
        session.commit()

@timer_databases
@timeit
def check_user_last_message(engine, user_id: int) -> Any:
    with sessionmaker(bind=engine)() as session:
        user_lm_record = session.get(Users_Last_Message, user_id)
        if user_lm_record:
            return user_lm_record.message_id
        else:
            return None
