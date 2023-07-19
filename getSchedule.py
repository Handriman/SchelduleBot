import datetime

import sh

wek = {'1': 'понедельник', '2': 'вторник', '3': 'среда', '4': 'четверг', '5': 'пятница', '6': 'суббота',
       '7': 'воскресенье', }


def normalize_date(bad_date: str) -> str:
    normal_date = '.'.join((bad_date.split('-'))[::-1][i] for i in range(0, 2))
    return normal_date

    pass


def get_day_schedule(schedule: dict) -> str:
    shift_date = datetime.datetime.now() - datetime.timedelta(days=120)

    current_date = normalize_date(str(shift_date.date()))

    result_string = wek[str(datetime.date.isoweekday(
        shift_date.date()))] + ', ' + current_date + '\n___________________________________\n '

    for el in schedule[current_date]:
        result_string = result_string + el + '\n------------------------------------------------------\n'
    print(current_date, )
    return result_string


def get_tomorrow_schedule(schedule: dict) -> str:
    shift_date = datetime.datetime.now() - datetime.timedelta(days=120)

    tomorrow_date = normalize_date(
        str((shift_date + datetime.timedelta(days=1)).date()))

    result_string = wek[str(datetime.date.isoweekday((shift_date + datetime.timedelta(
        days=1)).date()))] + ', ' + tomorrow_date + '\n___________________________________\n '

    for el in schedule[tomorrow_date]:
        result_string = result_string + el + '\n------------------------------------------------------\n'

    return result_string


def get_week_schedule(schedule: dict) -> tuple:
    shift_date = datetime.datetime.now() - datetime.timedelta(days=120)

    week_day = shift_date.date().isocalendar()[2]
    start_date = shift_date - datetime.timedelta(days=week_day - 1)

    dates = tuple(normalize_date(str((start_date + datetime.timedelta(days=i)).date())) for i in range(7))

    result_tuple = []
    for ind, date in enumerate(dates):
        final_string = wek[str(ind + 1)] + ', ' + date + '\n___________________________________\n '
        for el in schedule[date]:
            final_string += el + '\n------------------------------------------------------\n'

        result_tuple.append(final_string)

    return tuple(result_tuple)


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
