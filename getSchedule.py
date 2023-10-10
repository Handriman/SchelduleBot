from datetime import datetime, timedelta

wek = {'1': 'понедельник', '2': 'вторник', '3': 'среда', '4': 'четверг', '5': 'пятница', '6': 'суббота',
       '7': 'воскресенье', }
color_dict = {
    '(Лаб.  занятия - 17)': '🟠',
    '(Лекционные занятия)': '🔵',
    '(Практические занятия)': '🟢'
}
under_line = '\n___________________________________\n'
slashed_line = '------------------------------------------------------\n'


def normalize_date(bad_date: str) -> str:
    date_list = bad_date.split(' ')
    normal_date = '.'.join(date_list[0].split('-')[::-1][i] for i in range(0, 3))
    return normal_date


def colorize(lesson: dict) -> dict:
    lesson['type'] = color_dict[lesson['type']] + lesson['type']
    return lesson


def find_nearest(bad_date: datetime, schedule: dict) -> datetime | bool:
    keys = list(schedule.keys())
    date = bad_date
    counter: int = 0
    while counter <= 250:
        date += timedelta(days=1)

        normal_date = normalize_date(str(date))

        if normal_date in keys:
            if len(schedule[normal_date]) > 0:
                return date
    else:
        return False


def build_day(date: datetime, schedule: dict) -> str:
    current_normal_date = normalize_date(str(date.date()))

    schedule_list = schedule[current_normal_date]
    week_number = date.isocalendar()[1]
    if week_number % 2 == 0:
        odd = '(чт)'
    else:
        odd = '(нч)'
    output_sting = f'{odd} {wek[str(datetime.isoweekday(date))]}, {current_normal_date}{under_line}'

    for lesson in schedule_list:
        lesson = colorize(lesson)
        output_sting += f'''{lesson["time"]} | {lesson["location"]}\n
                            {lesson["subject"]}\n
                            {lesson["type"]}\n\n
                            {lesson["teacher"]}\n
                            {slashed_line}'''
    return output_sting


def get_day_schedule(schedule: dict) -> str:
    current_date = datetime.now()
    try:
        output_string = build_day(current_date, schedule)
    except KeyError:
        new_date = find_nearest(current_date, schedule)
        output_string = 'Ближайший учебный день:\n\n' + build_day(new_date, schedule)

    return output_string


def get_tomorrow_schedule(schedule: dict) -> str:
    tomorrow_date = datetime.now() + timedelta(days=1)
    try:
        output_string = build_day(tomorrow_date, schedule)
    except KeyError:
        new_date = find_nearest(tomorrow_date, schedule)
        output_string = 'Ближайший учебный день:\n\n' + build_day(new_date, schedule)

    return output_string


def get_week_schedule(schedule: dict) -> tuple:
    shift_date = datetime.now()

    week_day = shift_date.date().isocalendar()[2]
    start_date = shift_date - timedelta(days=week_day - 1)

    dates = tuple((start_date + timedelta(days=i)) for i in range(7))
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
        start_date = new_date - timedelta(days=week_day - 1)

        dates = tuple((start_date + timedelta(days=i)) for i in range(7))
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
    current_date = datetime.now()
    week_day = current_date.date().isocalendar()[2]
    start_date = current_date - timedelta(days=week_day - 1)
    start_date = start_date + timedelta(weeks=1)

    dates = tuple((start_date + timedelta(days=i)) for i in range(7))
    result_tuple = []
    for date in dates:
        try:
            output_string = build_day(date, schedule)
            result_tuple.append(output_string)
        except KeyError:
            pass

    if len(result_tuple) == 0:
        print(0000000)
        new_date = find_nearest(start_date, schedule)

        week_day = new_date.date().isocalendar()[2]
        start_date = new_date - timedelta(days=week_day - 1)

        dates = tuple((start_date + timedelta(days=i)) for i in range(7))
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


# def get_exam_schedule(schedule: dict) -> tuple[str]:
#     pass
