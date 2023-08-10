import datetime

import sh

wek = {'1': 'понедельник', '2': 'вторник', '3': 'среда', '4': 'четверг', '5': 'пятница', '6': 'суббота',
       '7': 'воскресенье', }


def normalize_date(bad_date: str) -> str:
    normal_date = '.'.join((bad_date.split('-'))[::-1][i] for i in range(0, 2))
    return normal_date

    pass


def find_nearest(schedule: dict, bad_date: str) -> str:

    keys = list(schedule.keys())
    return keys[0]




def get_day_schedule(schedule: dict) -> str:
    current_date = datetime.datetime.now()
    current_normal_date = normalize_date(str(current_date))
    try:
        schedule_list = schedule[current_normal_date]
        result_string = wek[str(datetime.date.isoweekday(
            current_date))] + ', ' + current_normal_date + '\n___________________________________\n '

        if len(schedule_list) != 0:
            for el in schedule_list:
                result_string = result_string + el + '\n------------------------------------------------------\n'
        else:
            result_string += 'Занятий нет, можно отдохнуть'
        return result_string
    except KeyError:
        ne_date = find_nearest(schedule, current_normal_date)
        schedule_list = schedule[ne_date]
        result_string = ne_date + '\n___________________________________\n '

        if len(schedule_list) != 0:
            for el in schedule_list:
                result_string = result_string + el + '\n------------------------------------------------------\n'
        else:
            result_string += 'Занятий нет, можно отдохнуть'
        return result_string


def get_tomorrow_schedule(schedule: dict) -> str:
    current_date = datetime.datetime.now()

    tomorrow_date = (current_date + datetime.timedelta(days=1)).date()
    normal_tomorrow = normalize_date(str(tomorrow_date))
    try:
        schedule_list = schedule[normal_tomorrow]
        result_string = wek[str(datetime.date.isoweekday(
            tomorrow_date))] + ', ' + normal_tomorrow + '\n___________________________________\n '

        if len(schedule_list) != 0:
            for el in schedule_list:
                result_string = result_string + el + '\n------------------------------------------------------\n'
        else:
            result_string += 'Занятий нет, можно отдохнуть'
        return result_string
    except KeyError:
        ne_date = find_nearest(schedule, normal_tomorrow)
        schedule_list = schedule[ne_date]
        result_string = ne_date + '\n___________________________________\n '

        if len(schedule_list) != 0:
            for el in schedule_list:
                result_string = result_string + el + '\n------------------------------------------------------\n'
        else:
            result_string += 'Занятий нет, можно отдохнуть'
        return result_string


def get_week_schedule(schedule: dict) -> tuple:
    shift_date = datetime.datetime.now()

    week_day = shift_date.date().isocalendar()[2]
    start_date = shift_date - datetime.timedelta(days=week_day - 1)

    dates = tuple(normalize_date(str((start_date + datetime.timedelta(days=i)).date())) for i in range(7))

    result_tuple = []
    try:
        for ind, date in enumerate(dates):
            final_string = wek[str(ind + 1)] + ', ' + date + '\n___________________________________\n '
            for el in schedule[date]:
                final_string += el + '\n------------------------------------------------------\n'

            result_tuple.append(final_string)

        return tuple(result_tuple)
    except:
        a = ['Пока учеба не началась, эта функция не работает']
        return tuple(a)


def get_nex_week_schedule() -> tuple:
    pass


def get_exam_schedule(schedule: dict) -> tuple[str]:
    pass


# @bot.message_handler(content_types=['text'])
# def schedule_today(message):
#     if message.text == 'Расписание на сегодня':
#         d = sh.get_day_schedule()
#         res = ''
#         temp = ''
#         for les in d:
#             if les != None:
#                 temp = '\n'.join(part for part in les)
#                 res = res + '\n' + temp
#         bot.send_message(message.chat.id, res)
#
#     if message.text == 'Расписание на неделю':
#
#         res = ''
#         week_days, dates = sh.get_week_schedule()
#         for i in range(len(dates)):
#             res = dates[i]
#             for lesson in week_days[i]:
#                 if lesson != None:
#                     temp = '\n'.join(str(part) for part in lesson)
#                     res = res + '\n' + temp
#             bot.send_message(message.chat.id, res)

if __name__ == "__main__":
    sched = sh.get_schedule_dict('schedule.json')

    print(get_week_schedule(sched))
