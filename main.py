import datetime
import logging
import os
import sqlite3
import threading
from time import sleep

import telebot
from telebot import types

import configure
import database
import getSchedule
from schedule import Schedule

logging.basicConfig(filename='bot.log', level=logging.INFO)

token = configure.config['token']

bot = telebot.TeleBot(token)
now_date = datetime.datetime.now()


def time_update():
    global now_date

    while True:
        schedule = Schedule()
        groups_numbers = os.listdir("groups")
        groups_numbers = [el[:-5] for el in groups_numbers]

        new = []
        for i, el in enumerate(groups_numbers):
            if 'old_' not in el:
                new.append(el)

        groups_numbers = new

        if (now_date + datetime.timedelta(hours=6)) < datetime.datetime.now():
            for group in groups_numbers:
                try:
                    flag = schedule.update_shedule(int(group))

                    if flag[0] and not flag[1]:
                        bot.send_message(384573724, f'Расписание обновлено, обнаружены изменения {group}')
                    elif not flag[0]:
                        bot.send_message(384573724, f'не удалсь обновить расписание группы {group}')

                except:
                    bot.send_message(384573724, 'Расписание не обновлено, ошибка')
                    pass
            now_date = datetime.datetime.now()

        else:
            sleep(10800)


thread1 = threading.Thread(target=time_update)


def create_record(message: types.Message, g: int) -> bool:
    connection = sqlite3.connect('bot_users.db')
    a = database.add_user(connection, tuple(
        [message.from_user.id, message.chat.id, message.from_user.first_name, message.from_user.last_name,
         message.from_user.username,
         g,
         datetime.datetime.now()]))
    return a


def edit_message(chat_id, message_id, text):
    bot.edit_message_text(text, chat_id=chat_id, message_id=message_id)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет')

    bot.send_message(message.chat.id, 'Напишите номер своей группы')
    bot.register_next_step_handler_by_chat_id(message.chat.id, register_user)


def register_user(message: types.Message):
    try:
        g = int(message.text)
    except ValueError:
        bot.send_message(message.chat.id, 'Неправильный номер группы')
        bot.register_next_step_handler_by_chat_id(message.chat.id, register_user)
        pass
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Расписание на сегодня')
    item2 = types.KeyboardButton('Расписание на завтра')
    item3 = types.KeyboardButton('Расписание на эту неделю')
    item4 = types.KeyboardButton('Расписание на следующую неделю')
    item5 = types.KeyboardButton('Изменить номер группы')
    markup.add(item1)
    markup.add(item2)
    markup.add(item3)
    markup.add(item4)
    markup.add(item5)

    create_record(message, g)
    bot.send_message(message.chat.id, 'Вы успешно, зарегистрировались', reply_markup=markup)


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


def isGroupExist(group: int) -> bool:
    groups_numbers = os.listdir("groups")
    groups_numbers = [el[:-5] for el in groups_numbers]

    new = []
    for i, el in enumerate(groups_numbers):
        if 'old_' not in el:
            new.append(el)

    groups_numbers = new

    if str(group) in groups_numbers:
        return True
    else:
        return False


@bot.message_handler(content_types=['text'])
def reply_on_text(message: types.Message):
    group = int(database.get_user_by_id(message.chat.id)[0][0])
    mainSchedule = Schedule()
    if message.text == 'Расписание на сегодня':
        if isGroupExist(group):
            schedule = mainSchedule.get_schedule(group=group)
            one_day_schedule = getSchedule.get_day_schedule(schedule)
            bot.send_message(message.chat.id, one_day_schedule)
        else:
            bot.send_message(message.chat.id, 'Кажется расписания для вашей группы нет, сейчас попробую его найти')
            res = mainSchedule.create_schedule(group=group)
            if res[0]:

                one_day_schedule = getSchedule.get_day_schedule(res[1])
                bot.send_message(message.chat.id, one_day_schedule)
            else:
                bot.send_message(message.chat.id, 'Что-то пошло не так, либо недоступен сайт тулгу, либо вашей группы '
                                                  'не существует, попробуйте изменить группу')

        logging.info(f'{message.from_user.first_name} {message.from_user.last_name},{message.chat.id}, TODAY')
    elif message.text == 'Расписание на завтра':
        if isGroupExist(group):
            schedule = mainSchedule.get_schedule(group=group)
            one_day_schedule = getSchedule.get_tomorrow_schedule(schedule)
            bot.send_message(message.chat.id, one_day_schedule)
        else:
            bot.send_message(message.chat.id, 'Кажется расписания для вашей группы нет, сейчас попробую его найти')
            res = mainSchedule.create_schedule(group=group)
            if res[0]:

                one_day_schedule = getSchedule.get_tomorrow_schedule(res[1])
                bot.send_message(message.chat.id, one_day_schedule)
            else:
                bot.send_message(message.chat.id, 'Что-то пошло не так, либо недоступен сайт тулгу, либо вашей группы '
                                                  'не существует, попробуйте изменить группу')

        logging.info(f'{message.from_user.first_name},{message.from_user.last_name},{message.chat.id}, TOMORROW')
    elif message.text == 'Расписание на эту неделю':
        if isGroupExist(group):
            schedule = mainSchedule.get_schedule(group)
            week_schedule = getSchedule.get_week_schedule(schedule)
            for day in week_schedule:
                bot.send_message(message.chat.id, day)
        else:
            bot.send_message(message.chat.id, 'Кажется расписания для вашей группы нет, сейчас попробую его найти')
            res = mainSchedule.create_schedule(group=group)
            if res[0]:

                week_schedule = getSchedule.get_week_schedule(res[1])
                for day in week_schedule:
                    bot.send_message(message.chat.id, day)
            else:
                bot.send_message(message.chat.id, 'Что-то пошло не так, либо недоступен сайт тулгу, либо вашей группы '
                                                  'не существует, попробуйте изменить группу')


        logging.info(f'{message.from_user.first_name} {message.from_user.last_name},{message.chat.id}, THIS_WEEK')
    elif message.text == 'Расписание на следующую неделю':
        if isGroupExist(group):
            schedule = mainSchedule.get_schedule(group)
            week_schedule = getSchedule.get_nex_week_schedule(schedule)
            for day in week_schedule:
                bot.send_message(message.chat.id, day)
        else:
            bot.send_message(message.chat.id, 'Кажется расписания для вашей группы нет, сейчас попробую его найти')
            res = mainSchedule.create_schedule(group=group)
            if res[0]:

                week_schedule = getSchedule.get_nex_week_schedule(res[1])
                for day in week_schedule:
                    bot.send_message(message.chat.id, day)
            else:
                bot.send_message(message.chat.id, 'Что-то пошло не так, либо недоступен сайт тулгу, либо вашей группы '
                                                  'не существует, попробуйте изменить группу')

        logging.info(f'{message.from_user.first_name} {message.from_user.last_name},{message.chat.id}, NEXT_WEEK')

    elif message.text == 'Изменить номер группы':
        bot.send_message(message.chat.id, 'Напишите новый номер группы')
        bot.register_next_step_handler_by_chat_id(message.chat.id, change_group)
    else:
        logging.info(f'{message.from_user.first_name} {message.from_user.last_name},{message.chat.id}, INVALID MESSAGE')


def change_group(message: types.Message):
    try:
        g = int(message.text)
    except ValueError:
        bot.send_message(message.chat.id, 'Неправильный номер группы, попробуйте еще раз')
        bot.register_next_step_handler_by_chat_id(message.chat.id, change_group)
        pass
    f = database.change_user_group_by_id(message.chat.id, g)
    if f:
        bot.send_message(message.chat.id, 'Группа успешно обновлена')


# sh.update_shedule()

thread2 = threading.Thread(target=bot.infinity_polling)
thread1.start()
thread2.start()
# bot.infinity_polling()
