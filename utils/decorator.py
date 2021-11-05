from django.core.handlers.wsgi import WSGIRequest

from logger import log


def info_logger(func):
    def wrapper(*args, **kwargs):
        if isinstance(args[0], WSGIRequest):
            log.info(str(list(str(args[0].META).split(','))[70::]))
            return func(*args, **kwargs)
        else:
            log.info(str(args[0]) + '\n')
        func(*args, **kwargs)
    return wrapper


def chained(func):
    def wrapper(self, *args, **kwargs):
        func(self, *args, **kwargs)
        return self
    return wrapper
