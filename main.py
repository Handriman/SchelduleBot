import telebot
from telebot import types

import configure

# bot = AsyncTeleBot(configure.config['token'])
# telebot.types.BotCommand('test_command', 'it\'s a test description for test command')
import getSchedule
import sh

token = configure.config['token']

bot = telebot.TeleBot(token)


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
    if message.text == 'Расписание на завтра':
        one_day_schedule = getSchedule.get_tomorrow_schedule(schedule)
        bot.send_message(message.chat.id, one_day_schedule)
    if message.text == 'Расписание на эту неделю':
        week_schedule = getSchedule.get_week_schedule(schedule)
        for day in week_schedule:
            bot.send_message(message.chat.id, day)




bot.infinity_polling()
