class BotBaseException(Exception):
    pass


class MissingConfigException(Exception):
    pass


class CallerNotAuthorized(BotBaseException):
    pass
