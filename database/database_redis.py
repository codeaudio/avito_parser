from redis import StrictRedis


class Redis:
    def __init__(self, host, port, password):
        self.host = host
        self.port = port
        self.password = password

    def connect(self):
        return StrictRedis(
            host=self.host,
            port=self.port,
            password=self.password,
            charset="utf-8",
            decode_responses=True
        )
