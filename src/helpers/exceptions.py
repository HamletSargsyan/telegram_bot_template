class BotException(Exception):
    pass


class NoResult(BotException):
    pass


class AlreadyExists(BotException):
    pass
