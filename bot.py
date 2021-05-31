import telebot
from dotenv import load_dotenv
from telebot import apihelper

from avitoparser import Avito
from config import POXY_LOGIN, PROXY_IP, PROXY_PASS, PROXY_PORT, TELEGRAM_TOKEN

load_dotenv()

apihelper.proxy = {
    'https': f'socks5://{POXY_LOGIN}:{PROXY_PASS}@{PROXY_IP}:{PROXY_PORT}'
}

bot = telebot.TeleBot(TELEGRAM_TOKEN)

INPUT_DICT = {}


@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(
        message.chat.id,
        "/start - запуск ввода данных для поиска \n"
        "/parse - запуск парсинга после ввода/последний запрос юзера"
    )


@bot.message_handler(commands=['start'])
def send_start(message):
    INPUT_DICT[message.from_user.id] = {}
    bot.reply_to(
        message,
        "Это парсер Авито. Заполните данные поиска. "
        "Обязательное поле - объект поиска. "
        "Необязательные - мин. цена, макс. цена, город, кол-во объявлений."
        " Минус(-) - пропустить необязательное поле. "
    )
    msg = bot.reply_to(message, "Введите объект поиcка")
    bot.register_next_step_handler(msg, process_search_step)


def process_search_step(message):
    try:
        search_object = str(message.text).strip()
        INPUT_DICT[message.from_user.id]['search_object'] = search_object
        bot.reply_to(message, 'Примеры ввода: sankt-peterburg, rossiya, moskva')
        msg = bot.reply_to(message, 'Введите город')
        bot.register_next_step_handler(msg, process_city_step)
    except Exception as e:
        bot.reply_to(e, 'ошибка')


def process_city_step(message):
    try:
        city = str(message.text).strip()
        if city == '-':
            city = ''
        INPUT_DICT[message.from_user.id]['city'] = city
        msg = bot.reply_to(message, 'мин. цена')
        bot.register_next_step_handler(msg, process_min_step)
    except Exception as e:
        bot.reply_to(e, 'ошибка')


def process_min_step(message):
    try:
        min_price = str(message.text).strip()
        if min_price == '-' or not str(min_price).isdigit():
            min_price = ''
        INPUT_DICT[message.from_user.id]['min_price'] = min_price
        msg = bot.reply_to(message, 'макс. цена')
        bot.register_next_step_handler(msg, process_max_step)
    except Exception as e:
        bot.reply_to(e, 'ошибка')


def process_max_step(message):
    try:
        max_price = str(message.text).strip()
        if max_price == '-' or not str(max_price).isdigit():
            max_price = ''
        INPUT_DICT[message.from_user.id]['max_price'] = max_price
        bot.reply_to(
            message, 'Кол-во объявлений. Минус(-) - все объявления на странице'
        )
        msg = bot.reply_to(message, 'кол-во объявлений')
        bot.register_next_step_handler(msg, process_max_object_step)
    except Exception as e:
        bot.register_next_step_handler(e, 'ошибка')


def process_max_object_step(message):
    try:
        max_object = str(message.text).strip()
        if max_object == '-' or not str(max_object).isdigit():
            max_object = None
        else:
            max_object = int(max_object)
        INPUT_DICT[message.from_user.id]['max_object'] = max_object
        msg = bot.reply_to(message, '/parse  -  начать парсинг')
        bot.register_next_step_handler(msg, send_parse_result)
    except Exception as e:
        bot.register_next_step_handler(e, 'ошибка')


@bot.message_handler(commands=['parse'])
def send_parse_result(message):
    parse = Avito()
    try:
        INPUT_DICT[message.from_user.id]
    except KeyError:
        bot.reply_to(message, 'Последний запрос не найден.')
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
    [bot.reply_to(message, ''.join(str(res))) for res in result[:input_dict.get('max_object')]]


bot.polling(none_stop=True, timeout=300)

