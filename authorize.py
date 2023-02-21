import logging
from functools import wraps
from exceptions import *

logger = logging.getLogger("BOT")


def check_privilige(chat_id, priv, raise_exception=False):
    """
    :param raise_exception: 是否抛出异常
    :param chat_id: 对话ID
    :param priv: 权限字符串
    :return:
    """
    if chat_id in [138148119, -1001247553753]:  # Me, 432
        return True
    if raise_exception:
        raise CallerNotAuthorized
    else:
        return False


def authorize(priv):
    """
    授权装饰器
    :param priv:需要的权限字符串
    :return:
    """

    def decorator(func):
        @wraps(func)
        def wrapper(bot, update, *args, **kwargs):
            chat_id = update.message.chat_id
            if not check_privilige(chat_id, priv):
                update.message.reply_text(
                    text="You are not authorized to use this command", quote=True)
                return
            return func(bot, update, *args, **kwargs)

        return wrapper

    return decorator
