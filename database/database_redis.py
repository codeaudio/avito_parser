from redis import StrictRedis

from logger import log


class Redis:
    def __init__(self, host: str, port: str, password: str):
        self.__host = host
        self.__port = port
        self.__password = password
        self.__connect = None

    def _connect(self):
        self.__connect = StrictRedis(
            host=self.__host,
            port=self.__port,
            password=self.__password,
            charset='utf-8',
            decode_responses=True
        )
        return self

    def get(self, message) -> dict:
        return dict(self.__connect.hgetall(message.from_user.id))

    def save(self, message, dictionary: dict) -> None:
        try:
            self.__connect.hmset(message.from_user.id, dictionary)
        except Exception as e:
            save = self.get(message)
            self.__connect.delete(message.from_user.id)
            self.__connect.hmset(message.from_user.id, dictionary.update(save))
            log.warning(e)
