import time
from config_data.config import ENABLE_TIMING


NUM_FUNC = [0]

def timeit(func):
    def wrapper(*args, **kwargs):
        if ENABLE_TIMING:
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f"Функция {func.__name__} выполнена за {elapsed_time:.4f} секунд")
            return result
        else:
            return func(*args, **kwargs)

    return wrapper

def timer_databases(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        if elapsed_time > 4:
            NUM_FUNC[0] += 1
        return result
    return wrapper

