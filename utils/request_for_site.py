from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from config_data import config


def start_browser() -> webdriver.Chrome:
    chrome_options = Options()
    chrome_options.binary_location = config.WEB_DRIVER_PATH
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-software-rasterizer")
    chrome_options.add_argument("--disable-images")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--remote-debugging-port=0")
    driver = webdriver.Chrome(options=chrome_options)
    return driver


def get_group_list(browser: webdriver.Chrome) -> dict:
    browser.get('https://voenmeh.ru/obrazovanie/timetables')

    select_elem = browser.find_element('id', 'studsCbxGroupNumber')

    select = Select(select_elem)

    group_list = select.options

    group_dict = {}
    for group in group_list:
        group_dict[str(group.text)] = group.get_attribute('value')

    browser.close()

    return group_dict


def get_schedule(browser, value_group: str) -> dict:
    browser.get('https://voenmeh.ru/obrazovanie/timetables')

    select_elem = browser.find_element('id', 'studsCbxGroupNumber')

    select = Select(select_elem)

    select.select_by_value(value_group)

    input_element = browser.find_element(By.NAME,
                                         'bShowTimetable')  # Замените 'your_element_id' на реальный id элемента

    # Кликаем на элемент
    input_element.click()

    tables = browser.find_elements(By.CLASS_NAME, 'timetable_table')
    schedule_table = {}

    for schedule in tables:
        schedule_table[schedule.text.split('\n')[0].lower()] = schedule.text

    browser.close()

    return schedule_table


def get_all_schedule_from_site(browser, group_value_list: list):
    browser.get('https://voenmeh.ru/obrazovanie/timetables')

    select_elem = browser.find_element('id', 'studsCbxGroupNumber')

    select = Select(select_elem)
    for group, group_value in group_value_list:

        schedule_table = {}
        select.select_by_value(str(group_value))

        input_element = browser.find_element(By.NAME,
                                             'bShowTimetable')  # Замените 'your_element_id' на реальный id элемента

        # Кликаем на элемент
        input_element.click()

        tables = browser.find_elements(By.CLASS_NAME, 'timetable_table')

        for schedule in tables:
            schedule_table[schedule.text.split('\n')[0].lower()] = schedule.text

        yield group, schedule_table

    browser.close()
