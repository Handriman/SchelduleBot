import json
from typing import Tuple, List, Any

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import datetime

from bs4 import BeautifulSoup

import time

wek = {'1': 'пн', '2': 'вт', '3': 'ср', '4': 'чт', '5': 'пт', '6': 'сб', '7': 'вс', }

day_in_month = {'01':31, '02':28, '03':31, '04':30, '05':31, '06':30, '07':31, '08':31, '09':30, '10':31, '11':30, '12':31}


class Lesson():
    def __init__(self, name, time, location, teacher, type):
        self.name = name
        self.time = time
        self.location = location
        self.teacher = teacher
        self.type = type


class Day():
    def __init__(self, lessons: list[Lesson]):
        self.lessons = lessons


def get_table_from_site(group: int) -> str:
    grp = group

    url = f'https://tulsu.ru/schedule/?search={grp}'

    driver = webdriver.Chrome()

    driver.get(url)

    table_selector = "table.schedule"  # Замените на селектор своей таблицы
    wait_time = 5000  # Замените на необходимое количество секунд

    try:
        table = WebDriverWait(driver, wait_time).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, table_selector))
        )
        table_data = table.get_attribute("outerHTML")
        # Здесь можно добавить код для обработки и анализа данных из таблицы\

        return table_data

    except:
        print("Произошла ошибка при ожидании загрузки таблицы.")

    # Закрытие браузера
    driver.quit()


def get_table_from_files(file_name: str):
    with open(file_name, 'r') as file:
        lines = file.readlines()

    result = ''.join(line for line in lines)
    return result


def transorm(column) -> list[str]:
    soup1 = BeautifulSoup(str(column), 'html.parser')

    # Проверяем наличие данных в столбце
    if soup1.select_one('.schedule-lessons div.schedule-lesson-info'):
        time_element = soup1.select_one('.schedule-lessons div.schedule-lesson-info:nth-of-type(3)').text.strip()
        subject_element = soup1.select_one('.schedule-lessons div.schedule-lesson-info:nth-of-type(1)').text.strip()
        lesson_type_element = soup1.select_one(
            '.schedule-lessons div.schedule-lesson-info:nth-of-type(2)').text.strip()
        cabinet_element = soup1.select_one('.schedule-lessons a[href^="/schedule/?search="]').text.strip()
        teacher_element = soup1.select_one('.schedule-lessons a[href^="/schedule/?search="]')
        if teacher_element:
            next_element = teacher_element.find_next('a')
            teacher_element = next_element.text.strip() if next_element else None

        # print('Время:', time_element)
        # print('Предмет:', subject_element)
        # print('Вид занятия:', lesson_type_element)
        # print('Преподаватель:', teacher_element)
        # print('Кабинет:', cabinet_element)
        lesson = [subject_element, time_element, cabinet_element, teacher_element, lesson_type_element]
        return lesson

    else:
        pass
        # print('Столбец пуст')


def get_dict(row1, row2, row3, row4, row5, row6, row7, row8, head) -> dict:
    result = {}

    for i in range(1, 148):
        temp = {head[i].text: [
            transorm(row1[i]),
            transorm(row2[i]),
            transorm(row3[i]),
            transorm(row4[i]),
            transorm(row5[i]),
            transorm(row6[i]),
            transorm(row7[i]),
            transorm(row8[i]),
        ]}
        result.update(temp)

    return result


def read_file(file_name: str):
    with open(file_name, 'r') as file:
        row = file.readlines()

    return row


def write_in_file(file_name: str, data) -> None:
    with open(file_name, 'w') as file:
        file.writelines(data)


def save_dict(dictionary: dict, file_name: str) -> None:
    with open(file_name, 'w') as file:
        json.dump(dictionary, file)


def load_dict(file_name: str) -> dict:
    with open(file_name, 'r') as file:
        sche = json.load(file)

    return sche


def update_shedule() -> None:
    data = get_table_from_site(121111)
    soup = BeautifulSoup(data, 'html.parser')
    rows = soup.find_all('tr')

    head = rows[0].find_all('th')

    row1 = rows[1].find_all('td')
    row2 = rows[2].find_all('td')
    row3 = rows[3].find_all('td')
    row4 = rows[4].find_all('td')
    row5 = rows[5].find_all('td')
    row6 = rows[6].find_all('td')
    row7 = rows[7].find_all('td')
    row8 = rows[8].find_all('td')

    d = get_dict(row1, row2, row3, row4, row5, row6, row7, row8, head)
    save_dict(d, 'schedule.json')


def get_day_schedule():
    d = load_dict('schedule.json')
    print(d)

    day_number = str(datetime.date.isoweekday(datetime.date.today()))
    date = str(datetime.date.today()).split('-')

    date = wek[day_number] + ', ' + str(date[2]) + '.' + str(date[1])

    print(date)
    print(d[date])
    return d[date]


def get_courent_day(day:str, num_day:int, schedule:dict):

    date = day.split('-')

    date = wek[str(num_day)] + ', ' + str(date[2]) + '.' + str(date[1])
    return schedule[date]


def get_all_week()->list[str]:
    week_day = datetime.datetime.now().isocalendar()[2]

    start_date = datetime.datetime.now() - datetime.timedelta(days=week_day)

    dates = [str((start_date + datetime.timedelta(days=i)).date()) for i in range(7)]
    return dates

def get_week_schedule() -> tuple[list[list], list[str]]:
    week_days  = []

    d = load_dict('schedule.json')
    dates: list[str] = get_all_week()

    for i in range(1, 7):

        week_days.append(get_courent_day(dates[i], i, d))
    dates.pop(0)

    return week_days, dates




print(get_week_schedule())














# d = get_dict(row1, row2, row3, row4,row5,row6,row7,row8,head)
# save_dict(d, 'schedule.json')
# print(d)

# update_shedule()
# get_day_schedule()
