# encoding: utf-8
import os
import logging
import sys

from telegram.ext import CommandHandler, ApplicationBuilder, ContextTypes, Application
from dotenv import load_dotenv
from exceptions import *
import steam_api
import config
import requests
import authorize
import telegram

load_dotenv()
PROXY_URL = None
TOKEN = None
STEAM_API_KEY = None
STEAM_API_ENABLE = True
steam_status = None
REQUEST_KWARGS = {
    'proxy_url': 'http://localhost:1080'
}
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("BOT")
formatter = logging.Formatter(
    "%(asctime)s - [%(name)s][%(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S")
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


async def cmd_start(update: telegram.Update, ctx: ContextTypes.DEFAULT_TYPE):
    await ctx.bot.send_message(update.effective_chat.id, text="Hello World\nVersion: v0.0.1\n")


async def post_init(app: Application):
    logger.info("Running bot @%s (%d)" %
                (app.bot.bot.username, app.bot.bot.id))
    logger.info("join_group: %s" % app.bot.bot.can_join_groups)
    logger.info("access_message: %s" % app.bot.bot.can_read_all_group_messages)


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


def load_config():
    global TOKEN, STEAM_API_KEY, PROXY_URL
    TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN',
                           None) or config.TELEGRAM_BOT_TOKEN
    PROXY_URL = os.environ.get('PROXY_URL', None)
    STEAM_API_KEY = os.environ.get(
        'STEAM_API_KEY', None) or config.STEAM_API_KEY
    if TOKEN is None:
        raise RuntimeError(
            "Token not set. Please set token in env or config.py")
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
    load_config()
    application = ApplicationBuilder().token(TOKEN).post_init(post_init)
    if PROXY_URL is not None:
        application = application.proxy_url(
            PROXY_URL).get_updates_proxy_url(PROXY_URL)
    application = application.build()
    # logger.info("About me: ID:%d username:%s" %
    #             (application.bot_data, aboutme.username))
    # application.add_handler(CommandHandler('clocker', clocker))
    # application.add_handler(CommandHandler('save_msg', save_msg))
    application.add_handler(CommandHandler('start', cmd_start))
    # application.add_handler(CommandHandler('owner_status', cmd_owner_status))
    # dispatcher.add_handler(MessageHandler(Filters.all, debug_catch))
    application.add_error_handler(error_handler)
    logger.info("Start polling")
    application.run_polling()
    print(application.bot.bot)
    return


if __name__ == "__main__":
    main()
