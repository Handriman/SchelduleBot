from time import sleep

import telebot
from telebot.async_telebot import AsyncTeleBot
from telebot import types
from telebot.types import KeyboardButton

import configure
import asyncio
import aiohttp
import sh

import selenium
from bs4 import BeautifulSoup

# bot = AsyncTeleBot(configure.config['token'])
# telebot.types.BotCommand('test_command', 'it\'s a test description for test command')


token = configure.config['token']

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Кнопка')
    item2 = types.KeyboardButton('Расписание на сегодня')
    markup.add(item1)
    markup.add(item2)
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
def schedule_today(message):
    if message.text == 'Расписание на сегодня':
        d = sh.get_day_schedule()
        res = ''
        temp = ''
        for les in d:
            if les != None:
                temp = '\n'.join(part for part in les)
                res = res + '\n' + temp
        bot.send_message(message.chat.id, res)

    if message.text == 'Расписание на неделю':

        res = ''
        week_days, dates = sh.get_week_schedule()
        for i in range(len(dates)):
            res = dates[i]
            for lesson in week_days[i]:
                if lesson != None:
                    temp = '\n'.join(str(part) for part in lesson)
                    res = res + '\n' + temp
            bot.send_message(message.chat.id, res)


@bot.message_handler(content_types=['text'])
def schedule_week(message):
    print('DLF:JDSJF:LKSDJ:FJK')



bot.infinity_polling()
