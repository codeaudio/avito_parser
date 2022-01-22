from redis import StrictRedis

from logger import log
from utils.decorator import chained, Adapter


class Redis:
    def __init__(self, host: str, port: str, password: str):
        self.__host = host
        self.__port = port
        self.__password = password
        self.__connect = None

    @chained
    def _connect(self):
        self.__connect = StrictRedis(
            host=self.__host,
            port=self.__port,
            password=self.__password,
            charset='utf-8',
            decode_responses=True
        )

    def get_keys(self):
        return self.__connect.scan_iter(match='*')

    def get_all(self) -> dict:
        data, keys = {}, self.get_keys()
        for key in keys:
            try:
                data[key] = self.__connect.hgetall(key)
            except Exception as e:
                log.warning((str(e) + f" {key}"))
        return data

    @Adapter.massage_to_user_id
    def get(self, message) -> dict:
        return dict(self.__connect.hgetall(message))

    @Adapter.massage_to_user_id
    def save(self, message, dictionary: dict) -> None:
        try:
            self.__connect.hmset(message, dictionary)
        except Exception as e:
            save = self.get(message)
            self.__connect.delete(message)
            self.__connect.hmset(message, dictionary.update(save))
            log.warning(e)

    def delete(self, user_id):
        self.__connect.delete(user_id)
