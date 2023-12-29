import datetime
import json
import logging
import sqlite3
import time
import os

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

import database
import getSchedule


class Schedule:
    _wek = {'1': 'пн', '2': 'вт', '3': 'ср', '4': 'чт', '5': 'пт', '6': 'сб', '7': 'вс', }

    _day_in_month = {'01': 31, '02': 28, '03': 31, '04': 30, '05': 31, '06': 30, '07': 31, '08': 31, '09': 30, '10': 31,
                     '11': 30, '12': 31}

    @staticmethod
    def _dwn_raw_table(group: int) -> str:
        url = f'https://tulsu.ru/schedule/'

        driver = webdriver.Chrome()

        driver.get(url)
        search_input = driver.find_element('css selector', '.search')
        search_input.send_keys(f'{group}')
        search_input.send_keys(Keys.ENTER)

        time.sleep(5)
        try:
            driver.find_element('css selector', '.isplay-mode header__item display-mode__list').send_keys(Keys.ENTER)
        except:
            pass

        table_selector = "table.schedule"  # Замените на селектор своей таблицы
        wait_time = 5000  # Замените на необходимое количество секунд

        try:
            table = WebDriverWait(driver, wait_time).until(
                ec.presence_of_element_located((By.CSS_SELECTOR, table_selector))
            )
            table_data = table.get_attribute("outerHTML")
            # Здесь можно добавить код для обработки и анализа данных из таблицы\
            driver.quit()
            return table_data

        except:
            print("Произошла ошибка при ожидании загрузки таблицы.")

        # Закрытие браузера
        driver.quit()

    # Получаем строку из

    def _transform(self, column) -> str:

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
                if part is None:
                    temp_lesson.pop(ind)

            lesson: str = '|'.join(part for part in temp_lesson)
            return lesson

        else:
            pass
            # print('Столбец пуст')

    def _get_dict(self, bad_rows, head) -> dict:
        result = {}
        for i in range(1, len(bad_rows[0])):
            final_rows = []
            for j in range(0, len(bad_rows)):
                final_rows.append(self._transform(bad_rows[j][i]))
            without_none = []
            for ind in range(len(final_rows)):
                if final_rows[ind] is not None:
                    without_none.append(final_rows[ind])
            final_rows = without_none
            new_list = []
            for les in final_rows:
                les_list = les.split('|')
                if len(les_list) == 5:
                    temp_dict = {
                        'time': les_list[0],
                        'subject': les_list[1],
                        'type': les_list[2],
                        'location': les_list[3],
                        'teacher': les_list[4]
                    }
                else:
                    temp_dict = {
                        'time': les_list[0],
                        'subject': les_list[1],
                        'type': les_list[2],
                        'location': les_list[3],
                        'teacher': 'Неизвестно'
                    }
                new_list.append(temp_dict)

            temp = {head[i].text[4::]: new_list}
            result.update(temp)

        return result

    def _save_dict(self, dictionary: dict, file_name: str) -> None:
        with open(f"groups/{file_name}", 'w') as file:
            json.dump(dictionary, file)

    def _load_dict(self, file_name: str) -> dict:
        with open(f"groups/{file_name}", 'r') as file:
            return json.load(file)

    def _fix_date(self, schedule: dict):

        first_year, second_year = 0, 0

        keys = list(schedule.keys())
        new_keys = []

        current_date = datetime.datetime.now()

        if 8 <= current_date.month <= 12:
            first_year = current_date.year
            second_year = first_year + 1
        elif 1 <= current_date.month < 8:
            second_year = current_date.year
            first_year = second_year - 1

        for i, key in enumerate(keys):
            month = int(key.split('.')[1])
            if 8 <= month <= 12:
                new_keys.append(key + '.' + str(first_year))
            elif 1 <= month < 8:
                new_keys.append(key + '.' + str(second_year))
        new_dict = {}
        for i in range(len(keys)):
            new_dict[new_keys[i]] = schedule[keys[i]]

        return new_dict

    def _compare(self, filename: str) -> bool:
        if not os.path.isfile(f"groups/old_{filename}"):
            d = self._load_dict(filename)
            self._save_dict(d, 'old_' + filename)
            return True
        else:
            new_dict = self._load_dict(filename)
            old_dict = self._load_dict('old_' + filename)
            if len(new_dict) != len(old_dict):
                self._save_dict(new_dict, 'old_' + filename)
                return False
            else:
                keys = list(new_dict.keys())
                for key in keys:
                    if old_dict[key] != new_dict[key]:
                        self._save_dict(new_dict, 'old_' + filename)
                        return False

                return True

    def update_shedule(self, group: int) -> (bool, bool):
        print('Starting update')
        res = self.create_schedule(group=group)
        if res[0]:
            f = self._compare(f'{group}.json')
            print(f)
            print('update complete')
            return True, f
        else:
            return False, False

    def create_schedule(self, group: int) -> (bool, dict):
        try:
            data: str = self._dwn_raw_table(group=group)

            soup = BeautifulSoup(data, 'html.parser')
            rows = soup.find_all('tr')

            head = rows[0].find_all('th')
            td_rows = []
            for i in range(1, len(rows)):
                td_rows.append(rows[i].find_all('td'))

            d = self._get_dict(td_rows, head)

            d = self._fix_date(d)
            # print(d)

            self._save_dict(d, f'{group}.json')
            return True, d
        except Exception as e:
            logging.critical(f'ошибка: {e}')
            return False, {}

    def get_schedule(self, group: str) -> dict:

        return self._load_dict(f"{group}.json")


if __name__ == "__main__":
    a = Schedule()
    # a.update_shedule('820321аф')
    d = a.get_schedule('121111')
    # b = getSchedule.build_day(date=datetime.date.today(), schedule=d)
    con = sqlite3.connect('bot_users.db')
    print(database.get_all_users(con))
