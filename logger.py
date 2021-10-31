import logging

logging.basicConfig(
    handlers=[logging.FileHandler('bot.log', 'w', 'utf-8')],
    format='%(asctime)s, %(levelname)s, %(message)s',
    datefmt='%m.%d.%y %H:%M',
    level=logging.INFO
)

log = logging.getLogger("logger")


def info_logger(func):
    def wrapper(*args, **kwargs):
        log.info(args[0])
        func(*args, **kwargs)
    return wrapper
