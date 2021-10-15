import html
from telegram import Chat, User, ParseMode
from telegram.error import BadRequest
from telegram.utils.helpers import mention_html
from telegram import ParseMode , Bot, Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext, CommandHandler, Filters, run_async, CallbackQueryHandler

from SaitamaRobot import dispatcher, REDIS, DEV_USERS, telethn
from SaitamaRobot.modules.disable import DisableAbleCommandHandler
from SaitamaRobot.modules.helper_funcs.chat_status import (
    bot_admin,
    user_admin
)
from SaitamaRobot.modules.helper_funcs.chat_status import user_can_change, user_admin_no_reply
from SaitamaRobot.modules.helper_funcs.extraction import extract_user_and_text
from SaitamaRobot.modules.helper_funcs.alternate import typing_action



@run_async
@typing_action
def approval(update: Update, context: CallbackContext) -> str:
    bot = context.bot
    args = context.args
    
    chat = update.effective_chat  
    user = update.effective_user 
    message = update.effective_message
    args = context.args 
    user_id, reason = extract_user_and_text(message, args)
    if not user_id:
        message.reply_text("You don't seem to be referring to a user.")
        return 
    try:
        member = chat.get_member(user_id)
    except BadRequest as excp:
        if excp.message == "User not found":
            message.reply_text("I can't seem to find this user")
            return 
        else:
            raise
    if user_id == context.bot.id:
        message.reply_text("How I supposed to approve myself")
        return 
    
    chat_id = str(chat.id)[1:] 
    approve_list = list(REDIS.sunion(f'approve_list_{chat_id}'))
    target_user = mention_html(member.user.id, member.user.first_name)
    if target_user in approve_list:
        message.reply_text(
            "{} is an approved user. Auto Warns, antiflood, and blocklists won't apply to them.".format(mention_html(member.user.id, member.user.first_name)),                                              
            parse_mode=ParseMode.HTML
        )
        return

    if target_user not in approve_list:
        message.reply_text(
            "{} is not an approved user. They are affected by normal commands.".format(mention_html(member.user.id, member.user.first_name)),                                              
            parse_mode=ParseMode.HTML
        )
        return



@run_async
@bot_admin
@user_admin
@typing_action
@user_can_change
def approve(update: Update, context: CallbackContext) -> str:
    bot = context.bot
    args = context.args
    
    chat = update.effective_chat  
    user = update.effective_user 
    message = update.effective_message
    args = context.args 
    user_id, reason = extract_user_and_text(message, args)
    if not user_id:
        message.reply_text("You don't seem to be referring to a user.")
        return
    member = chat.get_member(int(user_id))
    if member.status == 'administrator' or member.status == 'creator':
        message.reply_text(
            "User is already admin - locks, blocklists, and antiflood already don't apply to them.")
        return
    
    try:
        member = chat.get_member(user_id)
    except BadRequest as excp:
        if excp.message == "User not found":
            message.reply_text("I can't seem to find this user")
            return 
        else:
            raise
    if user_id == context.bot.id:
        message.reply_text("How I supposed to approve myself")
        return 
    
    chat_id = str(chat.id)[1:] 
    approve_list = list(REDIS.sunion(f'approve_list_{chat_id}'))
    target_user = mention_html(member.user.id, member.user.first_name)
    if target_user in approve_list:
        message.reply_text(
            "{} is already approved in {}.They will already now be ignored by automated admin actions like locks, blocklists, and antiflood.".format(mention_html(member.user.id, member.user.first_name),
                                                           chat.title),
            parse_mode=ParseMode.HTML
        )
        return
    member = chat.get_member(int(user_id))
    chat_id = str(chat.id)[1:]
    REDIS.sadd(f'approve_list_{chat_id}', mention_html(member.user.id, member.user.first_name))
    message.reply_text(
        "{} has been approved in {} They will now be ignored by automated admin actions like locks, blocklists, and antiflood.".format(mention_html(member.user.id, member.user.first_name),
                                                                     chat.title),
        parse_mode=ParseMode.HTML)
    
    

@run_async
@bot_admin
@user_admin
@user_can_change
@typing_action
def unapprove(update: Update, context: CallbackContext) -> str:
    bot = context.bot
    args = context.args
    
    chat = update.effective_chat  
    user = update.effective_user 
    message = update.effective_message
    args = context.args 
    user_id, reason = extract_user_and_text(message, args)
    if not user_id:
        message.reply_text("You don't seem to be referring to a user.")
        return 
    try:
        member = chat.get_member(user_id)
    except BadRequest as excp:
        if excp.message == "User not found":
            message.reply_text("I can't seem to find this user")
            return 
        else:
            raise
    if user_id == context.bot.id:
        message.reply_text("how I supposed to approve or unapprove myself")
        return 
    chat_id = str(chat.id)[1:] 
    approve_list = list(REDIS.sunion(f'approve_list_{chat_id}'))
    target_user = mention_html(member.user.id, member.user.first_name)
    if target_user not in approve_list:
        message.reply_text(
            "{} isn't approved yet.".format(mention_html(member.user.id, member.user.first_name)),
            parse_mode=ParseMode.HTML
        )
        return
    member = chat.get_member(int(user_id))
    chat_id = str(chat.id)[1:]
    REDIS.srem(f'approve_list_{chat_id}', mention_html(member.user.id, member.user.first_name))
    message.reply_text(
        "{} is no longer approved in {} automated admin actions like locks, blocklists, and antiflood will effect again.".format(mention_html(member.user.id, member.user.first_name),
                                                                     chat.title),
        parse_mode=ParseMode.HTML
    )

    
@run_async
@bot_admin
@user_admin
@typing_action
def approved(update: Update, context: CallbackContext) -> str:
    bot = context.bot
    args = context.args
    
    chat = update.effective_chat 
    user = update.effective_user 
    message = update.effective_message
    chat_id = str(chat.id)[1:] 
    approved_list = list(REDIS.sunion(f'approve_list_{chat_id}'))
    approved_list.sort()
    approved_list = ", ".join(approved_list)
    
    if approved_list: 
            message.reply_text(
                "The Following Users Are Approved: \n"
                "{}".format(approved_list),
                parse_mode=ParseMode.HTML
            )
    else:
        message.reply_text(
            "No users are are approved in {}.".format(chat.title),
                parse_mode=ParseMode.HTML
        )

def unapproveall(update, context):
    chat = update.effective_chat
    user = update.effective_user
    msg = update.effective_message

    chatmem = chat.get_member(user.id)
    if chatmem.status == "creator":
        chat_id = str(chat.id)[1:]
        approvedlist = list(REDIS.sunion(f'approve_list_{chat_id}'))
        if not approvedlist:
            msg.reply_text("No one is approved here")
            return
        else:
            msg.reply_text(
                "Do you really wanna Unapproved all user in this Chat??",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="Yes I'm sure️", callback_data="un_true"
                            )
                        ],
                        [
                            InlineKeyboardButton(
                                text="Cancel", callback_data="un_cancel"
                            )
                        ],
                    ]
                ),
            )

    else:
        msg.reply_text("This command can be only used by chat OWNER!")



@run_async
@user_admin_no_reply
def callback_button(update, context):
    query = update.callback_query
    message = query.message
    userid = update.effective_user.id
    match = query.data
    chat = update.effective_chat

    usermem = chat.get_member(userid).status

    if match == "un_cancel" and usermem == "creator":
        return query.message.edit_text("Cancelled Unapprove.")

    elif match == "un_true" and usermem == "creator":

        chat_id = str(chat.id)[1:] 
    approve_list = list(REDIS.sunion(f'approve_list_{chat_id}'))
    for target_user in approve_list:
        REDIS.srem(f'approve_list_{chat_id}', target_user)
        query.message.edit_text(f"Successfully Unapproved all user in this Chat.")
      

APPROVED_HANDLER = DisableAbleCommandHandler("approved", approved, filters=Filters.group)
UNAPPROVE_ALL_HANDLER = DisableAbleCommandHandler(["unapproveall", "disapproveall"], unapproveall, filters=Filters.group)
APPROVE_HANDLER = DisableAbleCommandHandler("approve", approve, pass_args=True, filters=Filters.group)
UNAPPROVE_HANDLER = DisableAbleCommandHandler(["unapprove", "disapprove"], unapprove, pass_args=True, filters=Filters.group)
APPROVEL_HANDLER = DisableAbleCommandHandler("approval", approval, pass_args=True, filters=Filters.group)
BUTTON_HANDLER = CallbackQueryHandler(callback_button, pattern="un_.*")


dispatcher.add_handler(APPROVED_HANDLER)
dispatcher.add_handler(UNAPPROVE_ALL_HANDLER)
dispatcher.add_handler(APPROVE_HANDLER) 
dispatcher.add_handler(UNAPPROVE_HANDLER) 
dispatcher.add_handler(APPROVEL_HANDLER)
dispatcher.add_handler(BUTTON_HANDLER)
