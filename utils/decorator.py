import json

from django.core.handlers.wsgi import WSGIRequest
from telebot.types import Message

from logger import log


class Adapter:

    @staticmethod
    def massage_to_user_id(func):
        def wrapper(self, *args):
            new_args = args
            if isinstance(args[0], Message):
                user_id = args[0].from_user.id
                if len(args) > 1:
                    new_args = tuple([user_id] + [element for element in args[1:]])
                    return func(self, *new_args)
                new_args = (user_id,)
            return func(self, *new_args)
        return wrapper


def info_logger(func):
    def wrapper(*args, **kwargs):
        if isinstance(args[0], WSGIRequest):
            try:
                log.info(
                    str(args[0].user) + ": " +
                    str(json.loads(args[0].body or json.dumps({}))) +
                    str(list(str(args[0].META).split(','))[70:])
                )
            except Exception as e:
                log.error(e)
            return func(*args, **kwargs)
        else:
            log.info(args[0])
            func(*args, **kwargs)
    return wrapper


def chained(func):
    def wrapper(self, *args, **kwargs):
        func(self, *args, **kwargs)
        return self
    return wrapper
