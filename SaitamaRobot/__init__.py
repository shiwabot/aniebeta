import logging
import os
import sys
import time
import spamwatch
from redis import StrictRedis

import telegram.ext as tg
from aiohttp import ClientSession
from pymongo import MongoClient
from telethon.sessions import StringSession
from telethon import TelegramClient
from Python_ARQ import ARQ
from pyrogram import Client, errors
from aiohttp import ClientSession
from motor.motor_asyncio import AsyncIOMotorClient as MongoClient
StartTime = time.time()

# enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('log.txt'),
              logging.StreamHandler()],
    level=logging.INFO)

LOGGER = logging.getLogger(__name__)

# if version < 3.6, stop bot.
if sys.version_info[0] < 3 or sys.version_info[1] < 6:
    LOGGER.error(
        "You MUST have a python version of at least 3.6! Multiple features depend on this. Bot quitting."
    )
    quit(1)

ENV = bool(os.environ.get('ENV', False))

if ENV:
    TOKEN = os.environ.get('TOKEN', None)

    try:
        OWNER_ID = int(os.environ.get('OWNER_ID', None))
    except ValueError:
        raise Exception("Your OWNER_ID env variable is not a valid integer.")

    JOIN_LOGGER = os.environ.get('JOIN_LOGGER', None)
    OWNER_USERNAME = os.environ.get("OWNER_USERNAME", None)

    try:
        SUDO_USERS = set(
            int(x) for x in os.environ.get("SUDO_USERS", "").split())
        DEV_USERS = set(int(x) for x in os.environ.get("DEV_USERS", "").split())
        ASSE_USERS = set(int(x) for x in os.environ.get("ASSE_USERS", "").split())
    except ValueError:
        raise Exception(
            "Your sudo or dev users list does not contain valid integers.")

    try:
        SUPPORT_USERS = set(
            int(x) for x in os.environ.get("SUPPORT_USERS", "").split())
    except ValueError:
        raise Exception(
            "Your support users list does not contain valid integers.")

    try:
        WHITELIST_USERS = set(
            int(x) for x in os.environ.get("WHITELIST_USERS", "").split())
    except ValueError:
        raise Exception(
            "Your whitelisted users list does not contain valid integers.")

    try:
        TIGER_USERS = set(
            int(x) for x in os.environ.get("TIGER_USERS", "").split())
    except ValueError:
        raise Exception(
            "Your tiger users list does not contain valid integers.")

    INFOPIC = bool(os.environ.get('INFOPIC', False))
    BOT_USERNAME = os.environ.get('BOT_USERNAME', None)
    EVENT_LOGS = os.environ.get('EVENT_LOGS', None)
    GBAN_LOGS = os.environ.get('GBAN_LOGS', None)
    WEBHOOK = bool(os.environ.get('WEBHOOK', False))
    URL = os.environ.get('URL', "")  # Does not contain token
    PORT = int(os.environ.get('PORT', 5000))
    CERT_PATH = os.environ.get("CERT_PATH")
    API_ID = os.environ.get('API_ID', None)
    API_HASH = os.environ.get('API_HASH', None)
    HEROKU_API_KEY = os.environ.get('HEROKU_API_KEY',None)
    BOT_NAME = os.environ.get('BOT_NAME',None)
    BOT_USERNAME = os.environ.get('BOT_USERNAME',None)
    HEROKU_APP_NAME = os.environ.get('HEROKU_APP_NAME',None)
    UPSTREAM_REPO_URL = os.environ.get('UPSTREAM_REPO_URL',None)
    MESSAGE_DUMP = os.environ.get('MESSAGE_DUMP',None)
    DB_URI = os.environ.get('DATABASE_URL')
    MONGO_DB_URI = os.environ.get('MONGO_DB_URI',None)
    MESSAGE_DUMP_CHAT = os.environ.get('MESSAGE_DUMP_CHAT',None)
    USERBOT_ID = os.environ.get('USERBOT_ID',None)
    SUDOERS = os.environ.get('SUDOERS',None)
    USERBOT_USERNAME = os.environ.get('USERBOT_USERNAME',None)
    USERBOT_NAME = os.environ.get('USERBOT_NAME',None)
    DONATION_LINK = os.environ.get('DONATION_LINK')
    TEMP_DOWNLOAD_DIRECTORY = os.environ.get('TEMP_DOWNLOAD_DIRECTORY',None)
    LOAD = os.environ.get("LOAD", "").split()
    NO_LOAD = os.environ.get("NO_LOAD", "translation").split()
    DEL_CMDS = bool(os.environ.get('DEL_CMDS', False))
    STRICT_GBAN = bool(os.environ.get('STRICT_GBAN', False))
    WORKERS = int(os.environ.get('WORKERS', 8))
    BAN_STICKER = os.environ.get('BAN_STICKER',
                                 'CAADAgADOwADPPEcAXkko5EB3YGYAg')
    ALLOW_EXCL = os.environ.get('ALLOW_EXCL', True)
    MONGO_URI = os.environ.get('MONGO_URI', None)
    MONGO_PORT = int(os.environ.get('MONGO_PORT', None))
    MONGO_DB = os.environ.get('MONGO_DB', None)
    CASH_API_KEY = os.environ.get('CASH_API_KEY', None)
    REM_BG_API_KEY = os.environ.get('REM_BG_API_KEY',None)
    TIME_API_KEY = os.environ.get('TIME_API_KEY', None)
    AI_API_KEY = os.environ.get('AI_API_KEY', None)
    AI_BID = os.environ.get('AI_BID', None)
    ARQ_API_URL = "https://thearq.tech"
    ARQ_API_KEY = "RUQBNQ-GJOJGU-LTHHJM-JADHXU-ARQ"
    WALL_API = os.environ.get('WALL_API', None)
    SUPPORT_CHAT = os.environ.get('SUPPORT_CHAT', None)
    SPAMWATCH_SUPPORT_CHAT = os.environ.get('SPAMWATCH_SUPPORT_CHAT', None)
    SPAMWATCH_API = os.environ.get('SPAMWATCH_API', None)
    REDIS_URL = os.environ.get('REDIS_URL')
    TEMPORARY_DATA = os.environ.get('TEMPORARY_DATA', None)
    BOT_ID = os.environ.get('BOT_ID', None)
    STRING_SESSION = os.environ.get('STRING_SESSION', None)
 
    try:
        BL_CHATS = set(int(x) for x in os.environ.get('BL_CHATS', "").split())
    except ValueError:
        raise Exception(
            "Your blacklisted chats list does not contain valid integers.")

else:
    from SaitamaRobot.config import Development as Config
    TOKEN = Config.TOKEN

    try:
        OWNER_ID = int(Config.OWNER_ID)
    except ValueError:
        raise Exception("Your OWNER_ID variable is not a valid integer.")

    JOIN_LOGGER = Config.JOIN_LOGGER
    OWNER_USERNAME = Config.OWNER_USERNAME

    try:
        SUDO_USERS = set(int(x) for x in Config.SUDO_USERS or [])
        DEV_USERS = set(int(x) for x in Config.DEV_USERS or [])
        ASSE_USERS = set(int(x) for x in Config.ASSE_USERS or [])
    except ValueError:
        raise Exception(
            "Your sudo or dev users list does not contain valid integers.")

    try:
        SUPPORT_USERS = set(int(x) for x in Config.SUPPORT_USERS or [])
    except ValueError:
        raise Exception(
            "Your support users list does not contain valid integers.")

    try:
        WHITELIST_USERS = set(int(x) for x in Config.WHITELIST_USERS or [])
    except ValueError:
        raise Exception(
            "Your whitelisted users list does not contain valid integers.")

    try:
        TIGER_USERS = set(int(x) for x in Config.TIGER_USERS or [])
    except ValueError:
        raise Exception(
            "Your tiger users list does not contain valid integers.")

    EVENT_LOGS = Config.EVENT_LOGS
    BOT_USERNAME = Config.BOT_USERNAME
    GBAN_LOGS = Config.GBAN_LOGS
    WEBHOOK = Config.WEBHOOK
    URL = Config.URL
    PORT = Config.PORT
    CERT_PATH = Config.CERT_PATH
    API_ID = Config.API_ID
    API_HASH = Config.API_HASH

    DB_URI = Config.SQLALCHEMY_DATABASE_URI
    MONGO_DB_URI = Config.MONGO_DB_URI
    DONATION_LINK = Config.DONATION_LINK
    TEMP_DOWNLOAD_DIRECTORY = Config.TEMP_DOWNLOAD_DIRECTORY
    LOAD = Config.LOAD
    NO_LOAD = Config.NO_LOAD
    DEL_CMDS = Config.DEL_CMDS
    STRICT_GBAN = Config.STRICT_GBAN
    WORKERS = Config.WORKERS
    BAN_STICKER = Config.BAN_STICKER
    ALLOW_EXCL = Config.ALLOW_EXCL
    CASH_API_KEY = Config.CASH_API_KEY
    TIME_API_KEY = Config.TIME_API_KEY
    HEROKU_API_KEY = Config.HEROKU_API_KEY
    HEROKU_APP_NAME = Config.HEROKU_APP_NAME
    REM_BG_API_KEY = Config.REM_BG_API_KEY
    MESSAGE_DUMP = Config.MESSAGE_DUMP
    AI_API_KEY = Config.AI_API_KEY
    WALL_API = Config.WALL_API
    SUPPORT_CHAT = Config.SUPPORT_CHAT
    SPAMWATCH_SUPPORT_CHAT = Config.SPAMWATCH_SUPPORT_CHAT
    SPAMWATCH_API = Config.SPAMWATCH_API
    INFOPIC = Config.INFOPIC
    TEMPORARY_DATA = Config.TEMPORARY_DATA
    STRING_SESSION = Config.STRING_SESSION
    BOT_ID = Config.BOT_ID
    BOT_NAME = Config.BOT_NAME
    BOT_USERNAME = Config.BOT_USERNAME
    SUDOERS = Config.SUDOERS
    USERBOT_ID = Config.USERBOT_ID
    USERBOT_USERNAME = Config.USERBOT_USERNAME
    MESSAGE_DUMP_CHAT = Config.MESSAGE_DUMP_CHAT
    UPSTREAM_REPO_URL = Config.UPSTREAM_REPO_URL

    try:
        BL_CHATS = set(int(x) for x in Config.BL_CHATS or [])
    except ValueError:
        raise Exception(
            "Your blacklisted chats list does not contain valid integers.")



SUDO_USERS.add(OWNER_ID)
DEV_USERS.add(OWNER_ID)
ASSE_USERS.add(OWNER_ID)
if not SPAMWATCH_API:
    sw = None
    LOGGER.warning("SpamWatch API key missing! recheck your config.")
else:
    sw = spamwatch.Client(SPAMWATCH_API)

REDIS = StrictRedis.from_url(REDIS_URL,decode_responses=True)
try:
    REDIS.ping()
    LOGGER.info("Your redis server is now alive!")
except BaseException:
    raise Exception("Your redis server is not alive, please check again.")

finally:
   REDIS.ping()
   LOGGER.info("Your redis server is now alive!")
arq = ARQ(ARQ_API_URL, ARQ_API_KEY)

ubot = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)
try:
    ubot.start()
except BaseException:
    print("Userbot Error ! Have you added a STRING_SESSION in deploying??")
    sys.exit(1)

print("SaitamaRobot): INITIALIZING AIOHTTP SESSION")
aiohttpsession = ClientSession()
    
api_id = API_ID
api_hash = API_HASH
updater = tg.Updater(TOKEN, workers=WORKERS, use_context=True)
telethn = TelegramClient("saitama", API_ID, API_HASH)
pbot = Client("saitamaPyro", api_id=API_ID, api_hash=API_HASH, bot_token=TOKEN)
mongo_client = MongoClient(MONGO_DB_URI)
db = mongo_client.SaitamaRobot

dispatcher = updater.dispatcher

SUDO_USERS = list(SUDO_USERS) + list(DEV_USERS) + list(ASSE_USERS)
DEV_USERS = list(DEV_USERS) +list(ASSE_USERS)
ASSE_USERS = list(ASSE_USERS)
WHITELIST_USERS = list(WHITELIST_USERS)
SUPPORT_USERS = list(SUPPORT_USERS)
TIGER_USERS = list(TIGER_USERS)

# Load at end to ensure all prev variables have been set
from SaitamaRobot.modules.helper_funcs.handlers import (CustomCommandHandler,
                                                        CustomMessageHandler,
                                                        CustomRegexHandler)

# make sure the regex handler can take extra kwargs
tg.RegexHandler = CustomRegexHandler
tg.CommandHandler = CustomCommandHandler
tg.MessageHandler = CustomMessageHandler
