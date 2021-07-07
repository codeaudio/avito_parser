import os

from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

POXY_LOGIN = os.getenv('POXY_LOGIN')

PROXY_PASS = os.getenv('PROXY_PASS')

PROXY_IP = os.getenv('PROXY_IP')

PROXY_PORT = os.getenv('PROXY_PORT')

AVITO_HEADERS = {
    'User-Agent': (
        'Mozilla/5.0 '
        '(Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36'
        ' (KHTML, like Gecko) '
        'Chrome/89.0.4389.82 Safari/537.36'
    )
}

AVITO_URL = 'https://www.avito.ru/'
