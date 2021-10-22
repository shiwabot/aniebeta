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

GBAN_ERRORS = { 
    "User is an administrator of the chat", 
    "Chat not found", 
    "Not enough rights to restrict/unrestrict chat member", 
    "User_not_participant", 
    "Peer_id_invalid", 
    "Group chat was deactivated", 
    "Need to be inviter of a user to kick it from a basic group", 
    "Chat_admin_required", 
    "Only the creator of a basic group can kick group administrators", 
    "Channel_private", "Not in the chat", 
    "Can't remove chat owner"
 }

UNGBAN_ERRORS = { 
     "User is an administrator of the chat", 
     "Chat not found", 
     "Not enough rights to restrict/unrestrict chat member", 
     "User_not_participant", 
     "Method is available for supergroup and channel chats only", 
     "Not in the chat", 
     "Channel_private", 
     "Chat_admin_required", 
     "Peer_id_invalid", 
     "User not found"
  }

  @run_async
  def gban(bot: Bot, update: Update, args: List[str]): 
      message = update.effective_message # type: Optional[Message] 
      chat = update.effective_chat

      user_id, reason = extract_user_and_text(message, args)

      if not user_id: 
          message.reply_text("You don't seem to be referring to a user.") 
          return

      if int(user_id) == OWNER_ID: 
              message.reply_text("Fuck Off🖕, Never Going to GBAN my Owner😡") 
              return

      if user_id == 920437078: 
              message.reply_text("There is no way I can gban this user.He is my Creator/Developer") 
              return

      if int(user_id) in DEV_USERS: 
              message.reply_text("With His Little Hand Someone Trying To Ban a Apologypse.") 
              return

      if int(user_id) in SUDO_USERS: 
              message.reply_text("Yay There is Nothing I Can Do Because This User is Scorpion And I Scare With Scorpions😫") 
              return





