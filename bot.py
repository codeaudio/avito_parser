import os

import telebot
from dotenv import load_dotenv

from avitoparser import Avito

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

bot = telebot.TeleBot(TELEGRAM_TOKEN)

INPUT_DICT = {}


@bot.message_handler(commands=['start'])
def send_start(message):
    bot.reply_to(
        message,
        "Это парсер Авито. Заоплните данные посика. "
        "Обязательное поле - объект поиска. "
        "Необязательные - мин. цена, макс. цена, город."
        " Минус(-) - пропустить необязательное поле "
    )
    msg = bot.reply_to(message, "Введите объект поиcка")
    bot.register_next_step_handler(msg, process_search_step)


def process_search_step(message):
    try:
        search_object = message.text
        INPUT_DICT['search_object'] = search_object
        bot.reply_to(message, 'Примеры ввода: sankt-peterburg, rossiya, moskva')
        msg = bot.reply_to(message, 'Введите город')
        bot.register_next_step_handler(msg, process_city_step)
    except Exception as e:
        bot.reply_to(e, 'ошибка')


def process_city_step(message):
    try:
        city = message.text
        if city == '-':
            city = ''
        INPUT_DICT['city'] = city
        msg = bot.reply_to(message, 'мин. цена')
        bot.register_next_step_handler(msg, process_min_step)
    except Exception as e:
        bot.reply_to(e, 'ошибка')


def process_min_step(message):
    try:
        min_price = message.text
        if min_price == '-':
            min_price = ''
        INPUT_DICT['min_price'] = min_price
        msg = bot.reply_to(message, 'макс. цена')
        bot.register_next_step_handler(msg, process_max_step)
    except Exception as e:
        bot.reply_to(e, 'ошибка')


def process_max_step(message):
    try:
        max_price = message.text
        if max_price == '-':
            max_price = ''
        INPUT_DICT['max_price'] = max_price
        msg = bot.reply_to(message, '/parse  -  начать пасринг')
        bot.register_next_step_handler(msg, send_parse_result)
    except Exception as e:
        bot.register_next_step_handler(e, send_parse_result)


@bot.message_handler(commands=['parse'])
def send_parse_result(message):
    parse = Avito()
    result = parse.city(
        INPUT_DICT.get('city')
    ).min_price(
        INPUT_DICT.get('min_price')
    ).max_price(
        INPUT_DICT.get('max_price')
    ).search_object(
        INPUT_DICT.get('search_object')
    ).get().parse()
    [bot.reply_to(message, ''.join(str(res))) for res in result]


bot.polling(none_stop=True, interval=2)
