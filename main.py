# encoding: utf-8
# type:ignore
import os
import logging
import sys
import time
from typing import Optional
from telegram.ext import CommandHandler, ApplicationBuilder, ContextTypes, Application
from dotenv import load_dotenv
from exceptions import *
from config import Config
import steam_api
import requests
import authorize
import telegram

load_dotenv()
PROXY_URL = None
TOKEN: Optional[str] = None
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


def load_config():
    Config.TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', None)
    Config.PROXY_URL = os.environ.get('PROXY_URL', None)
    Config.STEAM_API_KEY = os.environ.get('STEAM_API_KEY', None)
    if Config.TOKEN is None:
        raise MissingConfigException("bot token missing")
    if STEAM_API_KEY is None:
        logger.info('Steam api key is not set. Steam status will be disabled')
        STEAM_API_ENABLE = False
    return


def debug_catch(bot, update):
    logger.debug("Last Catch")
    logger.debug(update)


async def error_handler(update: Optional[object], ctx: ContextTypes.DEFAULT_TYPE) -> None:
    print("***************************")
    if isinstance(ctx.error, telegram.error.TimedOut):
        # 网络超时
        logger.error("网络超时，请检查网络连接")


def main():
    load_config()

    application = ApplicationBuilder().token(Config.TOKEN).post_init(post_init)
    if Config.PROXY_URL is not None:
        application = application.proxy_url(
            Config.PROXY_URL).get_updates_proxy_url(Config.PROXY_URL)
    application = application.build()
    # application.add_handler(CommandHandler('clocker', clocker))
    # application.add_handler(CommandHandler('save_msg', save_msg))
    application.add_handler(CommandHandler('start', cmd_start))
    # dispatcher.add_handler(MessageHandler(Filters.all, debug_catch))
    application.add_error_handler(error_handler)
    logger.info("Start polling")
    try:
        application.run_polling()
    except telegram.error.TimedOut:
        print("连接Telegram服务器超时，请检查网络连接")


if __name__ == "__main__":
    main()
