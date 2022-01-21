# AvitoParser
**Бот** телеграма для парсинга объявлений по заданным параметрам(что ищем, город, стоимость от и до, кол-во объявлений)
````
Бот реализовано в bot.py 
Логика обработки страницы реализована в avitoparser.py
Данные хранятся в редис. Реализовано в database_redis
Апи для для взаимодействия с редис реализовано в пакете api. 
На данный момент реализованы эндпоинты для получения всех данных и для получения данных по id с редис
````
* .env пример
* > socks5://{POXY_LOGIN}:{PROXY_PASS}@{PROXY_IP}:{PROXY_PORT}
````
TELEGRAM_TOKEN=TELEGRAM_TOKEN

POXY_LOGIN = POXY_LOGIN

PROXY_PASS = POXY_LOGIN

PROXY_IP = PROXY_IP

PROXY_PORT = PROXY_PORT

REDIS_HOST = REDIS_HOST

REDIS_PORT= REDIS_PORT

REDIS_PASSWORD = REDIS_PASSWORD
````
* запуск
````
redis - получение списка пользователей и иъ последнего запроса. При первом использовании бота создается словарь в редис
api/v1/redis/' -  'GET', 'POST'  
api/v1/redis/user_id  - 'GET', 'DELETE', 'PUT', 'PATCH'
````