import telebot
from avitoparser import Avito

bot = telebot.TeleBot('1894033956:AAGkD_yFVqY4E1s2-Qinw3hnTtuCsTzDSxs')

INPUT_DICT = {}


@bot.message_handler(commands=['help', 'start'])
def send_start(message):
    bot.reply_to(message,
                 "Это парсер Авито. Заоплните данные посика. Обязательное поле - объект поиска. Необязательные - мин. цена, макс. цена, город. Минус(-) - пропустить необязательное поле ")
    msg = bot.reply_to(message, "Введите объект посика")
    bot.register_next_step_handler(msg, process_search_step)


def process_search_step(message):
    try:
        search_object = message.text
        INPUT_DICT['search_object'] = search_object
        msg = bot.reply_to(message, 'Введите город')
        bot.register_next_step_handler(msg, process_city_step)
    except Exception as e:
        bot.reply_to(message, 'ошибка')


def process_city_step(message):
    try:
        city = message.text
        if city == '-':
            city = ''
        INPUT_DICT['city'] = city
        msg = bot.reply_to(message, 'мин. цена')
        bot.register_next_step_handler(msg, process_min_step)
    except Exception as e:
        bot.reply_to(message, 'ошибка')


def process_min_step(message):
    try:
        min_price = message.text
        if min_price == '-':
            min_price = ''
        INPUT_DICT['min_price'] = min_price
        msg = bot.reply_to(message, 'макс. цена')
        bot.register_next_step_handler(msg, process_max_step)
    except Exception as e:
        bot.reply_to(message, 'ошибка')


def process_max_step(message):
    try:
        max_price = message.text
        if max_price == '-':
            max_price = ''
        INPUT_DICT['max_price'] = max_price
        msg = bot.reply_to(message, '/parse  -  начать пасринг')
        bot.register_next_step_handler(msg, send_parse_result)
    except OverflowError as e:
        bot.register_next_step_handler(msg, send_parse_result)


@bot.message_handler(commands=['help', 'parse'])
def send_parse_result(message):
    parse = Avito()
    result = parse.city(INPUT_DICT.get('city')).min_price(INPUT_DICT.get('min_price')).max_price(INPUT_DICT.get('max_price')).search_object(INPUT_DICT.get('search_object')).get()
    [bot.reply_to(message, ''.join(str(res))) for res in result]


bot.polling(none_stop=True, interval=2)
