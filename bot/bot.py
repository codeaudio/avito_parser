import telebot
from pytils.translit import slugify
from telebot import apihelper

from avitoparser import Avito
from config.config import (POXY_LOGIN, PROXY_IP, PROXY_PASS, PROXY_PORT,
                           TELEGRAM_TOKEN, REDIS_HOST, REDIS_PORT, REDIS_PASSWORD)
from database.database_redis import Redis
from logger import log

apihelper.proxy = {
    'https': f'socks5://{POXY_LOGIN}:{PROXY_PASS}@{PROXY_IP}:{PROXY_PORT}'
}

bot = telebot.TeleBot(TELEGRAM_TOKEN)

redis = Redis(REDIS_HOST, REDIS_PORT, REDIS_PASSWORD)


def save(message, dictionary):
    try:
        redis.connect().hmset(message.from_user.id, dictionary)
    except Exception as e:
        log.warning(e)
        save = dict(redis.connect().get(message.from_user.id))
        redis.connect().delete(message.from_user.id)
        redis.connect().hmset(message.from_user.id, save.update(dictionary))


@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(
        message.from_user.id,
        '/start - запуск ввода данных для поиска \n'
        '/parse - запуск парсинга после ввода/последний запрос юзера \n'
        'вернуться назад можно, если написать название предведущего шага. Всего 5 шагов. Пример: второй шаг '
    )


@bot.message_handler(commands=['start'])
def send_start(message):
    bot.send_message(
        message.from_user.id,
        'Это парсер Авито. Заполните данные поиска. '
        'Обязательное поле - объект поиска. '
        'Необязательные - мин. цена, макс. цена, город, кол-во объявлений.'
        ' Минус(-) - пропустить необязательное поле. '
    )
    msg = bot.send_message(message.from_user.id, 'Введите объект поиска')
    bot.register_next_step_handler(msg, process_search_step)


def process_search_step(message, retry=False):
    try:
        if not retry:
            search_object = str(message.text).strip()
            save(message, {'search_object': search_object})
            bot.send_message(
                message.from_user.id,
                'Примеры ввода: sankt-peterburg/санкт-петербург, '
                'rossiya/россия, moskva/москва\n'
                'Если хотите вернуться назад, то напишите первый шаг'
            )
            log.info((message.from_user.id, str({'search_object': search_object})))
        msg = bot.reply_to(message, 'Введите город')
        bot.register_next_step_handler(msg, process_city_step)
    except Exception as e:
        log.error(msg=e)
        bot.reply_to(message, 'ошибка')


def process_city_step(message, retry=False):
    if str(message.text).lower() in ['первый шаг']:
        return send_start(message)
    try:
        if not retry:
            city = str(message.text).strip()
            if city == '-':
                city = ''
            save(message, {'city': slugify(city)})
            log.info((message.from_user.id, str({'city': city})))
        bot.send_message(
            message.from_user.id,
            'Если хотите вернуться назад, то напишите второй шаг'
        )
        msg = bot.reply_to(message, 'мин. цена')
        bot.register_next_step_handler(msg, process_min_step)
    except Exception as e:
        log.error(msg=e)
        bot.reply_to(message, 'ошибка')


def process_min_step(message, retry=False):
    if str(message.text).lower() in ['второй шаг']:
        return process_search_step(message, True)
    try:
        if not retry:
            min_price = str(message.text).strip()
            if min_price == '-' or not str(min_price).isdigit():
                min_price = ''
            save(message, {'min_price': min_price})
            log.info((message.from_user.id, str({'min_price': min_price})))
        bot.send_message(
            message.from_user.id,
            'Если хотите вернуться назад, то напишите третий шаг'
        )
        msg = bot.reply_to(message, 'макс. цена')
        bot.register_next_step_handler(msg, process_max_step)
    except Exception as e:
        log.error(msg=e)
        bot.reply_to(message, 'ошибка')


def process_max_step(message, retry=False):
    if str(message.text).lower() in ['третий шаг']:
        return process_city_step(message, True)
    try:
        if not retry:
            max_price = str(message.text).strip()
            if max_price == '-' or not str(max_price).isdigit():
                max_price = ''
            save(message, {'max_price': max_price})
            log.info((message.from_user.id, str({'max_price': max_price})))
        bot.send_message(
            message.from_user.id,
            'Если хотите вернуться назад, то напишите четвертый шаг'
        )
        bot.send_message(
            message.from_user.id, 'Кол-во объявлений. Минус(-) - все объявления на странице'
        )
        msg = bot.reply_to(message, 'кол-во объявлений')
        bot.register_next_step_handler(msg, process_max_object_step)
    except Exception as e:
        log.error(msg=e)
        bot.register_next_step_handler(e, 'ошибка')


def process_max_object_step(message, retry=False):
    if str(message.text).lower() in ['четвертый шаг']:
        return process_min_step(message, True)
    try:
        if not retry:
            max_object = str(message.text).strip()
            if max_object == '-' or not str(max_object).isdigit():
                max_object = ''
            else:
                max_object = int(max_object)
            save(message, {'max_object': max_object})
            log.info((message.from_user.id, str({'max_object': max_object})))
        bot.send_message(
            message.from_user.id,
            'Если хотите вернуться назад, то напишите пятый шаг'
        )
        msg = bot.send_message(message.from_user.id, '/parse  -  начать парсинг')
        bot.register_next_step_handler(msg, send_parse_result)
    except Exception as e:
        log.error(msg=e)
        bot.send_message(message.from_user.id, 'ошибка')


@bot.message_handler(commands=['parse'])
def send_parse_result(message):
    if str(message.text).lower() in ['пятый шаг']:
        return process_max_step(message, True)
    parse = Avito()
    try:
        redis.connect().hgetall(message.from_user.id)
    except KeyError as e:
        log.warning(msg=e)
        return bot.send_message(message.from_user.id, 'Последний запрос не найден')
    input_dict = redis.connect().hgetall(message.from_user.id)
    result = parse.city(
        input_dict.get('city')
    ).min_price(
        input_dict.get('min_price')
    ).max_price(
        input_dict.get('max_price')
    ).search_object(
        input_dict.get('search_object')
    ).get().parse()
    if len(result) == 0:
        log.warning(msg=(parse.__class__.__name__, result))
        return bot.send_message(message.from_user.id, "Ничего не найдено")
    limit = input_dict.get('max_object')
    limit = int(limit) if str(limit).isdigit() else None
    for res in result[:limit]:
        if len(res) > 2 and len(res[-1]) > 3900: res[-1] = res[-1][:3900] + '...'
        bot.send_message(message.from_user.id, '\n'.join(map(str, res)))
    log.info((message.from_user.id, str(result)))

bot.infinity_polling(timeout=1000, long_polling_timeout=2000)
