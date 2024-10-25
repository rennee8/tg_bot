from datetime import datetime
from typing import Any
from sqlalchemy import update
from sqlalchemy.orm import sessionmaker
from telebot.types import Message
from databases.tables import Groups, Update_Table_Date, Users
from loader import engine, lock
from utils.misc.request_for_site import start_browser, get_group_list


def check_groups_db(engine) -> None:
    with lock:
        with sessionmaker(bind=engine)() as session:

            if session.query(Groups).first() is None:
                browser = start_browser()
                group_dict = get_group_list(browser)
                for group, value_group in group_dict.items():
                    new_user = Groups(group=group, value_group=int(value_group))
                    session.add(new_user)

                session.add(Update_Table_Date(table_name=Groups.__tablename__))
                session.commit()
            elif (datetime.now() - session.query(Update_Table_Date).filter(
                    Update_Table_Date.table_name == 'groups').first().created_at).days:
                session.query(Groups).delete()
                browser = start_browser()
                group_dict = get_group_list(browser)
                for group, value_group in group_dict.items():
                    new_user = Groups(group=group, value_group=int(value_group))
                    session.add(new_user)

                stmt = update(Update_Table_Date).where(Update_Table_Date.table_name == Groups.__tablename__)
                session.execute(stmt)
                session.commit()


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


def get_value_group_from_db(engine, group_user: str) -> str:
    with sessionmaker(bind=engine)() as session:
        group_record = session.get(Groups, group_user)
        return str(group_record.value_group)


def check_user_db(engine, message: Message = None) -> bool:
    with sessionmaker(bind=engine)() as session:
        user_record = session.get(Users, message.from_user.id)
        if user_record is None:
            return False
        else:
            return True


def add_user_in_db(engine, message: Message):
    with sessionmaker(bind=engine)() as session:
        new_user = Users(id=message.from_user.id, user_name=message.from_user.username, group=message.text.upper())
        session.add(new_user)
        session.commit()


if __name__ == "__main__":
    # check_groups_db(engine=engine)
    # a = get_group_list_from_db(engine, 'str')
    # print(a)
    # a = get_value_group_from_db(engine, '09С41')
    # print(a)
    # check_user_db(engine)
    # add_user_in_db(engine, 12412452, 'huy', 'Е5м91')
    pass
