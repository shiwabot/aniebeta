import htmlfrom io 
import BytesIOfrom typing 
import Optional, List

import timefrom datetime 
import datetime

from telegram import Message, Update, Bot, User, Chat, ParseMode
from telegram.error import BadRequest, TelegramError
from telegram.ext import run_async, CommandHandler, MessageHandler, Filters
from telegram.utils.helpers import mention_html

import Angelina.modules.sql.global_bans_sql as sql
from Angelina import dispatcher, OWNER_ID, DEV_USERS, SUDO_USERS, SUPPORT_USERS, WHITELIST_USERS, GBAN_LOGS, STRICT_GBAN, spam_watch
from Angelina.modules.helper_funcs.chat_status import user_admin, is_user_admin
from Angelina.modules.helper_funcs.extraction import extract_user, extract_user_and_text
from Angelina.modules.helper_funcs.filters import CustomFilters
from Angelina.modules.helper_funcs.misc import send_to_list
from Angelina.modules.sql.users_sql import get_all_chats

GBAN_ENFORCE_GROUP = 6



