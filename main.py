import telebot
from telebot import types
import datetime
import configure
import threading
import logging


# bot = AsyncTeleBot(configure.config['token'])
# telebot.types.BotCommand('test_command', 'it\'s a test description for test command')
import getSchedule
import sh

logging.basicConfig(filename='bot.log', level=logging.DEBUG, )

token = configure.config['token']

bot = telebot.TeleBot(token)
now_date = datetime.datetime.now()


def time_update():
    global now_date

    while True:
        if (now_date + datetime.timedelta(hours=12)) < datetime.datetime.now():
            try:
                sh.update_shedule()
            except:
                pass
            now_date = datetime.datetime.now()


thread1 = threading.Thread(target=time_update)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Расписание на сегодня')
    item2 = types.KeyboardButton('Расписание на завтра')
    item3 = types.KeyboardButton('Расписание на эту неделю')
    item4 = types.KeyboardButton('Расписание на следующую неделю')
    markup.add(item1)
    markup.add(item2)
    markup.add(item3)
    markup.add(item4)
    bot.send_message(message.chat.id, 'Выберите что вам надо', reply_markup=markup)


@bot.message_handler(commands=['button'])
def button_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Кнопка')
    item2 = types.KeyboardButton('Расписание на сегодня')
    item3 = types.KeyboardButton('Расписание на неделю')
    markup.add(item1)
    markup.add(item2)
    markup.add(item3)

    bot.send_message(message.chat.id, 'Выберите что вам надо', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def reply_on_text(message):
    schedule = sh.get_schedule_dict('schedule.json')
    if message.text == 'Расписание на сегодня':
        one_day_schedule = getSchedule.get_day_schedule(schedule)
        bot.send_message(message.chat.id, one_day_schedule)
        print(f'{message.from_user.first_name} {message.from_user.last_name}, на сегодня')
        logging.info(f'{message.from_user.first_name} {message.from_user.last_name}, на сегодня')
    if message.text == 'Расписание на завтра':
        one_day_schedule = getSchedule.get_tomorrow_schedule(schedule)
        bot.send_message(message.chat.id, one_day_schedule)
        print(f'{message.from_user.first_name} {message.from_user.last_name}, на завтра')
        logging.info(f'{message.from_user.first_name} {message.from_user.last_name}, на завтра')
    if message.text == 'Расписание на эту неделю':
        week_schedule = getSchedule.get_week_schedule(schedule)
        for day in week_schedule:
            bot.send_message(message.chat.id, day)
        print(f'{message.from_user.first_name} {message.from_user.last_name}, на неделю')
        logging.info(f'{message.from_user.first_name} {message.from_user.last_name}, на неделю')
    if message.text == 'Расписание на следующую неделю':
        bot.send_message(message.chat.id, 'Функция в разработке')
        print(f'{message.from_user.first_name} {message.from_user.last_name}, на след неделю')
        logging.info(f'{message.from_user.first_name} {message.from_user.last_name}, на след неделю')


thread2 = threading.Thread(target=bot.infinity_polling)

thread1.start()
thread2.start()
# bot.infinity_polling()
