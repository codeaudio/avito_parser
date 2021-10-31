from redis import StrictRedis


class Redis:
    def __init__(self, host, port, password):
        self.__host = host
        self.__port = port
        self.__password = password

    def connect(self):
        return StrictRedis(
            host=self.__host,
            port=self.__port,
            password=self.__password,
            charset="utf-8",
            decode_responses=True
        )
