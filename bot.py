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
    INPUT_DICT[message.from_user.id] = {}
    bot.reply_to(
        message,
        "Это парсер Авито. Заоплните данные посика. "
        "Обязательное поле - объект поиска. "
        "Необязательные - мин. цена, макс. цена, город, кол-во обявлений."
        " Минус(-) - пропустить необязательное поле "
    )
    msg = bot.reply_to(message, "Введите объект поиcка")
    bot.register_next_step_handler(msg, process_search_step)


def process_search_step(message):
    try:
        search_object = message.text
        INPUT_DICT[message.from_user.id]['search_object'] = search_object
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
        INPUT_DICT[message.from_user.id]['city'] = city
        msg = bot.reply_to(message, 'мин. цена')
        bot.register_next_step_handler(msg, process_min_step)
    except Exception as e:
        bot.reply_to(e, 'ошибка')


def process_min_step(message):
    try:
        min_price = message.text
        if min_price == '-':
            min_price = ''
        INPUT_DICT[message.from_user.id]['min_price'] = min_price
        msg = bot.reply_to(message, 'макс. цена')
        bot.register_next_step_handler(msg, process_max_step)
    except Exception as e:
        bot.reply_to(e, 'ошибка')


def process_max_step(message):
    try:
        max_price = message.text
        if max_price == '-':
            max_price = ''
        INPUT_DICT[message.from_user.id]['max_price'] = max_price
        bot.reply_to(
            message, 'Кол-во объявлений. Минус(-) - все объявления на странице'
        )
        msg = bot.reply_to(message, 'кол-во объявлений')
        bot.register_next_step_handler(msg, process_max_object_step)
    except Exception as e:
        bot.register_next_step_handler(e, process_max_object_step)


def process_max_object_step(message):
    try:
        max_object = message.text
        if max_object == '-':
            max_object = None
        INPUT_DICT[message.from_user.id]['max_object'] = max_object
        msg = bot.reply_to(message, '/parse  -  начать пасринг')
        bot.register_next_step_handler(msg, send_parse_result)
    except Exception as e:
        bot.register_next_step_handler(e, send_parse_result)


@bot.message_handler(commands=['parse'])
def send_parse_result(message):
    parse = Avito()
    try:
        INPUT_DICT[message.from_user.id]
    except KeyError:
        bot.reply_to(message, 'вы еще не отправляли запросы')
        return None
    input_dict = INPUT_DICT[message.from_user.id]
    result = parse.city(
        input_dict.get('city')
    ).min_price(
        input_dict.get('min_price')
    ).max_price(
        input_dict.get('max_price')
    ).search_object(
        input_dict.get('search_object')
    ).get().parse()
    [bot.reply_to(message, ''.join(str(res))) for res in result[:input_dict['max_object']]]


bot.polling(none_stop=True, interval=1)
