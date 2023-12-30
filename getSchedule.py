import datetime

import weather

wek = {'1': 'понедельник', '2': 'вторник', '3': 'среда', '4': 'четверг', '5': 'пятница', '6': 'суббота',
       '7': 'воскресенье', }
color_dict = {
    '(Лаб.  занятия - 17)': '🟠',
    '(Лекционные занятия)': '🔵',
    '(Практические занятия)': '🟢',
    '(зч)': '🔴',
    '(ДЗ)': '🔴',
    '(Экзамен)': '🔴',
    '(КР)': '🔴',
    '(КП)': '🔴',
    '(ДЗ по практике)': '🔴',
    '(Консультации)': '🔴',

}
under_line = '\n___________________________________\n'
slashed_line = '------------------------------------------------------\n'

exam_types = ['(Консультации)', '(зч)', '(ДЗ)', '(Экзамен)', '(КР)', '(КП)', '(ДЗ по практике)']


def normalize_date(bad_date: str) -> str:
    date_list = bad_date.split(' ')
    normal_date = '.'.join(date_list[0].split('-')[::-1][i] for i in range(0, 3))
    return normal_date


def colorize(lesson: dict) -> dict:

    temp_type = lesson['type']
    lesson['type'] = color_dict[temp_type] + temp_type
    return lesson


def find_nearest(bad_date: datetime.datetime, schedule: dict) -> datetime.datetime:
    keys = list(schedule.keys())
    flag = True
    date = bad_date
    normal_date = normalize_date(str(date))
    while True:
        date += datetime.timedelta(days=1)

        normal_date = normalize_date(str(date))

        if normal_date in keys:
            if len(schedule[normal_date]) > 0:
                return date


def build_day(date: datetime.datetime, schedule: dict):
    w = weather.get_day_weather(f'{date}'.split(' ')[0])

    current_normal_date = normalize_date(str(date))

    schedule_list = schedule[current_normal_date]
    week_number = date.isocalendar()[1]
    odd = ''
    if week_number % 2 == 0:
        odd = '(чт)'
    else:
        odd = '(нч)'
    if w != None:
        output_sting = f'{odd} {wek[str(datetime.datetime.isoweekday(date))]}, {current_normal_date[:-5]} 🌡 {w["min_max"][1]} \\ {w["min_max"][0]}{under_line}'
    else:
        output_sting = f'{odd} {wek[str(datetime.datetime.isoweekday(date))]}, {current_normal_date[:-5]}{under_line}'

    for lesson in schedule_list:
        lesson = colorize(lesson)

        if w != None:
            try:
                hour_w = w[lesson["time"][:5]]
            except Exception:
                hour_w = ['', '', '', '', '', '', '']
            output_sting += f'{lesson["time"]}  🌡 {hour_w[0]}({hour_w[1]})  Осадки: {hour_w[2]}%\n{lesson["location"]}\n{lesson["type"]}\n{lesson["subject"]}\n{lesson["teacher"]}\n{slashed_line}'
        else:
            output_sting += f'{lesson["time"]} | {lesson["location"]}\n{lesson["subject"]}\n{lesson["type"]}\n{lesson["teacher"]}\n{slashed_line}'
    return output_sting


def get_day_schedule(schedule: dict) -> str:
    current_date = datetime.datetime.now()
    try:
        output_string = build_day(current_date, schedule)
        print('ошибка, не могу найти эту дату, почему-то')
    except KeyError:
        new_date = find_nearest(current_date, schedule)
        output_string = 'Ближайший учебный день:\n\n' + build_day(new_date, schedule)

    return output_string


def get_tomorrow_schedule(schedule: dict) -> str:
    tomorrow_date = datetime.datetime.now() + datetime.timedelta(days=1)
    try:
        output_string = build_day(tomorrow_date, schedule)
    except KeyError:
        new_date = find_nearest(tomorrow_date, schedule)
        output_string = 'Ближайший учебный день:\n\n' + build_day(new_date, schedule)

    return output_string


def get_week_schedule(schedule: dict) -> tuple:
    shift_date = datetime.datetime.now()

    week_day = shift_date.date().isocalendar()[2]
    start_date = shift_date - datetime.timedelta(days=week_day - 1)

    dates = tuple((start_date + datetime.timedelta(days=i)).date() for i in range(7))
    result_tuple = []
    for date in dates:
        try:
            output_string = build_day(date, schedule)
            result_tuple.append(output_string)
        except KeyError:
            pass

    if len(result_tuple) == 0:
        new_date = find_nearest(start_date, schedule)

        week_day = new_date.date().isocalendar()[2]
        start_date = new_date - datetime.timedelta(days=week_day - 1)

        dates = tuple((start_date + datetime.timedelta(days=i)).date() for i in range(7))
        result_tuple = ['Ближайшая учебная неделя:']
        for date in dates:
            try:
                output_string = build_day(date, schedule)
                result_tuple.append(output_string)
            except KeyError:
                pass
        return tuple(result_tuple)
    else:
        return tuple(result_tuple)


def get_nex_week_schedule(schedule: dict) -> tuple:
    current_date = datetime.datetime.now()
    week_day = current_date.date().isocalendar()[2]
    start_date = current_date - datetime.timedelta(days=week_day - 1)
    start_date = start_date + datetime.timedelta(weeks=1)

    dates = tuple((start_date + datetime.timedelta(days=i)).date() for i in range(7))
    result_tuple = []
    for date in dates:
        try:
            output_string = build_day(date, schedule)
            result_tuple.append(output_string)
        except KeyError:
            pass

    if len(result_tuple) == 0:
  
        new_date = find_nearest(start_date, schedule)

        week_day = new_date.date().isocalendar()[2]
        start_date = new_date - datetime.timedelta(days=week_day - 1)

        dates = tuple((start_date + datetime.timedelta(days=i)).date() for i in range(7))
        result_tuple = ['Ближайшая учебная неделя:']
        for date in dates:
            try:
                output_string = build_day(date, schedule)
                result_tuple.append(output_string)
            except KeyError:
                pass
        return tuple(result_tuple)
    else:
        return tuple(result_tuple)


def get_exam_schedule(schedule: dict[list[dict]]) -> tuple[datetime] | tuple[str]:
    keys = list(schedule.keys())
    exam_dates = []
    for item in schedule.items():
        for lesson in item[1]:
            if lesson['type'] in exam_types:
                print(lesson, item[0])
                day, month, year = item[0].split('.')

                # Преобразовать строки в целочисленные значения
                day, month, year = int(day), int(month), int(year)

                # Создать экземпляр datetime.date
                date_obj = datetime.date(year, month, day)
                if date_obj not in exam_dates:
                    exam_dates.append(date_obj)

    if len(exam_dates) == 0:
        return tuple(['Сессия не найдена'])
    else:
        res_tuple = []
        for date in exam_dates:
            res_tuple.append(build_day(date, schedule))

        return tuple(res_tuple)


def get_nearest_exem(today: datetime.datetime, schedule: dict[list[dict]]) -> tuple[str]:
    exam_dates = []
    for item in schedule.items():
        for lesson in item[1]:
            if lesson['type'] in exam_types:
                print(lesson)
                day, month, year = item[0].split('.')

                # Преобразовать строки в целочисленные значения
                day, month, year = int(day), int(month), int(year)

                # Создать экземпляр datetime.date
                date_obj = datetime.datetime(year, month, day)
                exam_dates.append(date_obj)
    if len(exam_dates) == 0:
        return tuple(['Сессия не найдена'])
    else:
        res_tuple = []
        for date in exam_dates:
            if date >= today:
                res_tuple.append(build_day(date, schedule))

        return tuple(res_tuple)

