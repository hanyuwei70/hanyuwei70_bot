# encoding: utf-8
from config import TELEGRAM_BOT_TOKEN
import os, logging, sys

from telegram.ext import Updater

TOKEN = None
logger = logging.getLogger(__name__)
formatter = logging.Formatter("%(asctime)s - [%(name)s][%(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S")
loghandler = logging.StreamHandler(sys.stdout)
loghandler.setFormatter(formatter)
if os.environ.get('DEBUG', False):
    logger.setLevel(logging.DEBUG)
    loghandler.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)
    loghandler.setLevel(logging.INFO)
logger.addHandler(loghandler)


def clocker(bot, update):
    pass

def loadconfig():
    global TOKEN
    TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', None) or TELEGRAM_BOT_TOKEN
    if TOKEN is None:
        raise RuntimeError("Token not set. Please set token in env or config.py")
    return


def main():
    loadconfig()
    updaterhandle = Updater(token=TOKEN)
    aboutme=updaterhandle.bot.get_me()
    logger.info("About me: ID:%d username:%s" % (aboutme['id'], aboutme['username']))
    return


if __name__ == "__main__":
    main()
