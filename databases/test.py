import time
from random import randint
from databases.databases_action import check_user_last_message, \
    get_group_from_db, check_user_db
from loader import engine
from threading import Thread

from utils.decorators import NUM_FUNC

threads = []


def start_function():
    for _ in range(100):
        choice = randint(0, 2)
        if choice == 0:
            check_user_last_message(engine, randint(1, 100000))
        elif choice == 1:
            get_group_from_db(engine, randint(1, 1000000))
        elif choice == 2:
            check_user_db(engine, randint(1, 1000000))
        time.sleep(0.05)


for _ in range(1000):
    thread  = Thread(target=start_function)
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()

print(f'Функций завершившихся более 4х секунд: {NUM_FUNC[0]}')