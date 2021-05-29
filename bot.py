import telebot
from avitoparser import Avito

bot = telebot.TeleBot('1894033956:AAGkD_yFVqY4E1s2-Qinw3hnTtuCsTzDSxs')


@bot.message_handler(commands=['start', 'help'])
def send_parse_result(message):
    parse = Avito()
    result = parse.city('').min_price('').max_price('').search_object('камри').get()
    [bot.reply_to(message, ''.join(str(res))) for res in result]


bot.polling(none_stop=True, interval=2)
