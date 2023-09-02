import datetime
import logging
import sqlite3
import threading
from time import sleep

import telebot
from telebot import types

import configure
import database
import getSchedule
import sh

logging.basicConfig(filename='bot.log', level=logging.INFO)

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
        else:
            sleep(21600)


thread1 = threading.Thread(target=time_update)


def create_record(message: types.Message) -> bool:
    connection = sqlite3.connect('bot_users.db')
    a = database.add_user(connection, tuple(
        [message.from_user.id, message.chat.id, message.from_user.first_name, message.from_user.last_name,
         message.from_user.username,
         datetime.datetime.now()]))
    return a


def edit_message(chat_id, message_id, text):
    bot.edit_message_text(text, chat_id=chat_id, message_id=message_id)


@bot.message_handler(commands=['start'])
def start_message(message):
    create_record(message)

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

@bot.message_handler(commands=['all_users'])
def get_users(message):
    con = sqlite3.connect('bot_users.db')
    l = database.get_all_users(con)
    fs = ''
    for x in l:
        fs += f'{x[3]}, {x[4]}, {x[5]}, {x[1]}\n'

    bot.send_message(message.chat.id, fs)

@bot.message_handler(commands=['button'])
def button_message(message):
    create_record(message)
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
    create_record(message)
    schedule = sh.get_schedule_dict('schedule.json')
    if message.text == 'Расписание на сегодня':
        one_day_schedule = getSchedule.get_day_schedule(schedule)
        bot.send_message(message.chat.id, one_day_schedule)

        logging.info(f'{message.from_user.first_name} {message.from_user.last_name},{message.chat.id}, TODAY')
    elif message.text == 'Расписание на завтра':
        one_day_schedule = getSchedule.get_tomorrow_schedule(schedule)
        bot.send_message(message.chat.id, one_day_schedule)

        logging.info(f'{message.from_user.first_name},{message.from_user.last_name},{message.chat.id}, TOMORROW')
    elif message.text == 'Расписание на эту неделю':
        week_schedule = getSchedule.get_week_schedule(schedule)
        for day in week_schedule:
            bot.send_message(message.chat.id, day)

        logging.info(f'{message.from_user.first_name} {message.from_user.last_name},{message.chat.id}, THIS_WEEK')
    elif message.text == 'Расписание на следующую неделю':
        week_schedule = getSchedule.get_nex_week_schedule(schedule)
        for day in week_schedule:
            bot.send_message(message.chat.id, day)

        logging.info(f'{message.from_user.first_name} {message.from_user.last_name},{message.chat.id}, NEXT_WEEK')
    else:
        logging.info(f'{message.from_user.first_name} {message.from_user.last_name},{message.chat.id}, INVALID MESSAGE')


# sh.update_shedule()

thread2 = threading.Thread(target=bot.infinity_polling)
thread1.start()
thread2.start()
# bot.infinity_polling()
