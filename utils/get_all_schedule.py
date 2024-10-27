from databases.databases_action import get_all_values_group_form_db, add_schedule_in_db
from loader import bot, engine
from utils.request_for_site import get_all_schedule_from_site, start_browser

def get_all_schedule():
    group_value_list = get_all_values_group_form_db(engine)
    for group, schedule in get_all_schedule_from_site(start_browser(), group_value_list):
        add_schedule_in_db(engine=engine, type_act='add', group=group, schedule_dict=schedule)

if __name__ == "__main__":
    get_all_schedule()