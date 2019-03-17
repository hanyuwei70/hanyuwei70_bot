# encoding: utf-8
import os, logging, sys

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import telegram
from exceptions import *
import message, steam_api, config, requests, authorize

TOKEN = None
STEAM_API_KEY = None
STEAM_API_ENABLE = True
steam_status = None
REQUEST_KWARGS = {
    'proxy_url': 'http://localhost:1080'
}
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("BOT")
formatter = logging.Formatter("%(asctime)s - [%(name)s][%(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S")
loghandler = logging.StreamHandler(sys.stdout)
loghandler.setFormatter(formatter)
if logging.getLogger().getEffectiveLevel() == logging.INFO:
    logger.propagate = False
if os.environ.get('DEBUG', False):
    logger.setLevel(logging.DEBUG)
    loghandler.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)
    loghandler.setLevel(logging.INFO)
logger.addHandler(loghandler)


def clocker(bot, update, args):
    """
    处理定时提醒相关的命令
    :param bot: bot handle
    :param update: 更新
    :return:
    """
    update.message.reply_text("Not implemented")


@authorize.authorize('save_msg')
def save_msg(bot, update, args):
    """
    :param bot:
    :param update:
    :return:
    """
    logger.debug("Processing leave_msg")
    chat_id = update.message.chat.id
    message_id = update.message.message_id
    user = update.message['from']
    print(update.message.from_user)
    logger.info("saving message %d %d for %s" % (chat_id, message_id, user))
    if update.message.reply_to_message is not None:
        print("get reply msg")
        print(update.message.reply_to_message)
    else:
        print("get direct msg")
        print(update.message.text)
    update.message.reply_text(text="Received", quote=True)
    print(update)
    # TODO:save message


def cmd_start(bot, update):
    bot.send_message(chat_id=update.message.chat.id, text="Hello World!\nUnder development\nv0.0.1")


@authorize.authorize('status1')
def cmd_owner_status(bot, update):
    """
    找我在哪里（
    :param bot:
    :param update:
    :return:
    """
    global steam_status, STEAM_API_KEY, STEAM_API_ENABLE
    if steam_status is None and STEAM_API_ENABLE:
        try:
            steam_status = steam_api.SteamAPI(api_key=STEAM_API_KEY)
            STEAM_API_ENABLE = True
        except requests.HTTPError as e:
            logger.error('Steam API error! %s' % e)
    rep_txt = ""
    steam_res = steam_status.query_user_status(76561198057735328)
    rep_txt += "Steam:%s\n" % steam_res
    update.message.reply_text(text=rep_txt, quote=True)


def loadconfig():
    global TOKEN, STEAM_API_KEY
    TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', None) or config.TELEGRAM_BOT_TOKEN
    STEAM_API_KEY = os.environ.get('STEAM_API_KEY', None) or config.STEAM_API_KEY
    if TOKEN is None:
        raise RuntimeError("Token not set. Please set token in env or config.py")
    if STEAM_API_KEY is None:
        logger.info('Steam api key is not set. Steam status will be disabled')
        STEAM_API_ENABLE = False
    return


def debug_catch(bot, update):
    logger.debug("Last Catch")
    logger.debug(update)


def error_handler(bot, update, error):
    logger.error(error)


def main():
    loadconfig()
    updaterhandle = Updater(token=TOKEN, request_kwargs=REQUEST_KWARGS)
    aboutme = updaterhandle.bot.get_me()
    logger.info("About me: ID:%d username:%s" % (aboutme['id'], aboutme['username']))
    dispatcher = updaterhandle.dispatcher
    dispatcher.add_handler(CommandHandler('clocker', clocker, pass_args=True))
    dispatcher.add_handler(CommandHandler('save_msg', save_msg, pass_args=True))
    dispatcher.add_handler(CommandHandler('start', cmd_start))
    dispatcher.add_handler(CommandHandler('owner_status', cmd_owner_status))
    dispatcher.add_handler(MessageHandler(Filters.all, debug_catch))
    dispatcher.add_error_handler(error_handler)
    logger.info("Start polling")
    updaterhandle.start_polling()
    return


if __name__ == "__main__":
    main()
