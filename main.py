# encoding: utf-8
from config import TELEGRAM_BOT_TOKEN
import os, logging, sys

from telegram.ext import Updater, CommandHandler
import telegram

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
    """
    处理定时提醒相关的命令
    :param bot: bot handle
    :param update: 更新
    :return:
    """
    userid = update['from']['id']
    chatid = update['message']['chat']['chatid']
    username = update['from']['username']
    text = update['text']
    logger.info("got update: From:%s(%d) %s"%(username,userid,text))
    if text == "/clocker":
        bot.send_message(chat_id=chatid, text="提醒服务~", reply_markup=telegram.ReplyKeyboardMarkup(["查看"]))


def loadconfig():
    global TOKEN
    TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', None) or TELEGRAM_BOT_TOKEN
    if TOKEN is None:
        raise RuntimeError("Token not set. Please set token in env or config.py")
    return


def main():
    loadconfig()
    updaterhandle = Updater(token=TOKEN)
    aboutme = updaterhandle.bot.get_me()
    logger.info("About me: ID:%d username:%s" % (aboutme['id'], aboutme['username']))
    dispatcher = updaterhandle.dispatcher
    dispatcher.add_handler(CommandHandler('clocker', clocker))
    updaterhandle.start_polling()
    return


if __name__ == "__main__":
    main()
