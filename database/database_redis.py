from accessify import private
from redis import StrictRedis

from logger import log


class Redis:
    def __init__(self, host, port, password):
        self.__host = host
        self.__port = port
        self.__password = password
        self.__connect = None

    def _connect(self):
        self.__connect = StrictRedis(
            host=self.__host,
            port=self.__port,
            password=self.__password,
            charset="utf-8",
            decode_responses=True
        )
        return self

    def get(self, message):
        return dict(self.__connect.hgetall(message.from_user.id))

    def save(self, message, dictionary):
        try:
            self.__connect.hmset(message.from_user.id, dictionary)
        except Exception as e:
            log.warning(e)
            save = dict(self.__connect.get(message.from_user.id))
            self.__connect.delete(message.from_user.id)
            self.__connect.hmset(message.from_user.id, dictionary.update(save))
