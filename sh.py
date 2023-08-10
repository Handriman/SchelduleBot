import datetime
import json
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

wek = {'1': 'пн', '2': 'вт', '3': 'ср', '4': 'чт', '5': 'пт', '6': 'сб', '7': 'вс', }

day_in_month = {'01': 31, '02': 28, '03': 31, '04': 30, '05': 31, '06': 30, '07': 31, '08': 31, '09': 30, '10': 31,
                '11': 30, '12': 31}


# Получаем таблицу с сайта в HTML формате
def dwn_raw_table(group: int) -> str:
    url = f'https://tulsu.ru/schedule/'

    driver = webdriver.Chrome()

    driver.get(url)
    search_input = driver.find_element('css selector', '.search')
    search_input.send_keys(f'{group}')
    search_input.send_keys(Keys.ENTER)
    time.sleep(5)

    table_selector = "table.schedule"  # Замените на селектор своей таблицы
    wait_time = 5000  # Замените на необходимое количество секунд

    try:
        table = WebDriverWait(driver, wait_time).until(
            ec.presence_of_element_located((By.CSS_SELECTOR, table_selector))
        )
        table_data = table.get_attribute("outerHTML")
        # Здесь можно добавить код для обработки и анализа данных из таблицы\

        return table_data

    except:
        print("Произошла ошибка при ожидании загрузки таблицы.")

    # Закрытие браузера
    driver.quit()


# Получаем строку из
def get_data_from_json(file_name: str) -> str:
    with open(file_name, 'r') as file:
        lines = file.readlines()

    result = ''.join(line for line in lines)
    return result


def transform(column) -> str:
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
        temp_lesson = [time_element, subject_element, lesson_type_element, cabinet_element, teacher_element]
        for ind, part in enumerate(temp_lesson):
            if part == None: temp_lesson.pop(ind)

        lesson = '\n'.join(part for part in temp_lesson)
        return lesson

    else:
        pass
        # print('Столбец пуст')


# def get_dict(row1, row2, row3, row4, row5, row6, row7, row8, head) -> dict:
def get_dict(bad_rows, head) -> dict:
    result = {}
    for i in range(1, len(bad_rows[0])):
        final_rows = []
        for j in range(0, len(bad_rows)):
            final_rows.append(transform(bad_rows[j][i]))

        without_none = []
        for ind in range(len(final_rows)):
            if final_rows[ind] is not None:
                without_none.append(final_rows[ind])
        final_rows = without_none
        temp = {head[i].text[4::]: final_rows}
        result.update(temp)
    return result

    # for i in range(1, 148):
    #     final_rows = [
    #         transform(row1[i]),
    #         transform(row2[i]),
    #         transform(row3[i]),
    #         transform(row4[i]),
    #         transform(row5[i]),
    #         transform(row6[i]),
    #         transform(row7[i]),
    #         transform(row8[i]),
    #     ]
    #     # print(final_rows)
    #     without_none = []
    #     for ind in range(len(final_rows)):
    #         if final_rows[ind] is not None:
    #             without_none.append(final_rows[ind])
    #     final_rows = without_none
    #     temp = {head[i].text[4::]: final_rows}
    #     result.update(temp)
    # print(result)
    # return result


def save_dict(dictionary: dict, file_name: str) -> None:
    with open(file_name, 'w') as file:
        json.dump(dictionary, file)


def get_schedule_dict(file_name: str) -> dict:
    with open(file_name, 'r') as file:
        return json.load(file)


def update_shedule() -> None:
    data = dwn_raw_table(121111)
    soup = BeautifulSoup(data, 'html.parser')
    rows = soup.find_all('tr')

    head = rows[0].find_all('th')
    td_rows = []
    for i in range(1, len(rows)):
        td_rows.append(rows[i].find_all('td'))
    # row1 = rows[1].find_all('td')
    # row2 = rows[2].find_all('td')
    # row3 = rows[3].find_all('td')
    # row4 = rows[4].find_all('td')
    # row5 = rows[5].find_all('td')
    # row6 = rows[6].find_all('td')
    # row7 = rows[7].find_all('td')
    # row8 = rows[8].find_all('td')

    # d = get_dict(row1, row2, row3, row4, row5, row6, row7, row8, head)
    d = get_dict(td_rows, head)
    print(d)
    save_dict(d, 'schedule.json')


def get_day_schedule():
    d = get_schedule_dict('schedule.json')
    print(d)

    day_number = str(datetime.date.isoweekday(datetime.date.today()))
    date = str(datetime.date.today()).split('-')

    date = wek[day_number] + ', ' + str(date[2]) + '.' + str(date[1])

    print(date)
    print(d[date])
    return d[date]


def get_courent_day(day: str, num_day: int, schedule: dict):
    date = day.split('-')

    date = wek[str(num_day)] + ', ' + str(date[2]) + '.' + str(date[1])
    return schedule[date]


def get_all_week() -> list[str]:
    week_day = datetime.datetime.now().isocalendar()[2]

    start_date = datetime.datetime.now() - datetime.timedelta(days=week_day)

    dates = [str((start_date + datetime.timedelta(days=i)).date()) for i in range(7)]
    return dates


def get_week_schedule() -> tuple[list[list], list[str]]:
    week_days = []

    d = get_schedule_dict('schedule.json')
    dates: list[str] = get_all_week()

    for i in range(1, 7):
        week_days.append(get_courent_day(dates[i], i, d))
    dates.pop(0)

    return week_days, dates


# print(get_week_schedule())


if __name__ == "__main__":
    update_shedule()
# d = get_dict(row1, row2, row3, row4,row5,row6,row7,row8,head)
# save_dict(d, 'schedule.json')
# print(d)

# update_shedule()
# get_day_schedule()
