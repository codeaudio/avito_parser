from logger import log


def info_logger(func):
    def wrapper(*args, **kwargs):
        log.info(args[0])
        func(*args, **kwargs)
    return wrapper


def chained(func):
    def wrapper(self, *args, **kwargs):
        func(self, *args, **kwargs)
        return self
    return wrapper
