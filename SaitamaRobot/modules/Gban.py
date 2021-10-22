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

      if int(user_id) in SUPPORT_USERS: 
              message.reply_text("Wew You Are Trying To Ban A Mortal So Sed:/") 
              return 

       if int(user_id) in WHITELIST_USERS: 
              message.reply_text("I Can't Ban a Knight.") 
              return

       if user_id == bot.id: 
              message.reply_text("-_- So funny, lets gban myself why don't I? Nice try.") 
              return

       try: 
              user_chat = bot.get_chat(user_id) 
           except BadRequest as excp: 
              message.reply_text(excp.message)
              return

       if user_chat.type != 'private': 
              message.reply_text("That's not a user!") 
              return
      
       if sql.is_user_gbanned(user_id): if not reason: 
              message.reply_text("This user is already gbanned; I'd change the reason, but you haven't given me one...") 
              return

           old_reason = sql.update_gban_reason(user_id, user_chat.username or user_chat.first_name, reason) 
           if old_reason: 
              message.reply_text("This user is already gbanned, for the following reason:\n" 
                                 "<code>{}</code>\n" 
                                 "I've gone and updated it with your new reason!".format(html.escape(old_reason)), parse_mode=ParseMode.HTML) 
           else:
               message.reply_text("This user is already gbanned, but had no reason set; I've gone and updated")
     
           return 

       message.reply_text("*Getting Ready To GBAN*")

       start_time = time.time() 
       datetime_fmt = "%H:%M - %d-%m-%Y" 
       current_time = datetime.utcnow().strftime(datetime_fmt) 

       if chat.type != 'private': 
           chat_origin = "<b>{} ({})</b>\n".format(html.escape(chat.title), chat.id)
       else:
           chat_origin = "<b>{}</b>\n".format(chat.id)

       banner = update.effective_user # type: Optional[User] 
       log_message = ( 
                    "<b>Global Ban</b>" \ 
                    "\n#GBANNED" \ 
                    "\n<b>Originated from:</b> {}" \ 
                    "\n<b>Status:</b> <code>Enforcing</code>" \ 
                    "\n<b>Scorpion User:</b> {}" \ 
                    "\n<b>User:</b> {}" \ 
                    "\n<b>ID:</b> <code>{}</code>" \ 
                    "\n<b>Event Stamp:</b> {}" \ 
                    "\n<b>Reason:</b> {}".format(chat_origin, mention_html(banner.id, banner.first_name), 
                                                 mention_html(user_chat.id, user_chat.first_name), 
                                                              user_chat.id, current_time, reason or "No reason given")) 









