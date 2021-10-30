import logging

logging.basicConfig(
    handlers=[logging.FileHandler('bot.log', 'w', 'utf-8')],
    format='%(levelname)s: %(message)s',
    datefmt='%m-%d %H:%M',
    level=logging.INFO
)
log = logging.getLogger("logger")
