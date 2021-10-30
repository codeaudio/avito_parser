import redis


class Redis:
    def __init__(self, host, port, password):
        self.host = host
        self.port = port
        self.password = password

    def connect(self):
        return redis.StrictRedis(
            host=self.host,
            port=self.port,
            password=self.password,
            charset="utf-8",
            decode_responses=True
        )
