import html

from telegram import ParseMode, Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.error import BadRequest
from telegram.ext import CallbackContext, CommandHandler, Filters, run_async, CallbackQueryHandler, MessageHandler
from telegram.utils.helpers import mention_html, mention_markdown, escape_markdown
import SaitamaRobot.modules.sql.notes_sql as sql
from SaitamaRobot import SUDO_USERS, dispatcher, DEV_USERS, WHITELIST_USERS
from SaitamaRobot.modules.disable import DisableAbleCommandHandler
from SaitamaRobot.modules.helper_funcs.chat_status import (bot_admin, can_pin,
                                                           can_promote,
                                                           connection_status,
                                                           user_admin,
                                                           ADMIN_CACHE, user_admin_no_reply, promote_permission)
from SaitamaRobot.modules.helper_funcs.extraction import (extract_user,
                                                          extract_user_and_text)
from SaitamaRobot.modules.log_channel import loggable
from SaitamaRobot.modules.helper_funcs.alternate import send_message
import SaitamaRobot.modules.sql.feds_sql as sql
from SaitamaRobot.modules.helper_funcs.extraction import (extract_unt_fedban,
                                                          extract_user,
                                                          extract_user_fban)
from SaitamaRobot.modules.helper_funcs.msg_types import get_message_type
from SaitamaRobot.modules.helper_funcs.misc import build_keyboard_alternate
from SaitamaRobot.modules.log_channel import loggable
from SaitamaRobot.modules.connection import connected
from SaitamaRobot.modules.sql import admin_sql as sql
from SaitamaRobot.modules.helper_funcs.alternate import send_message
from SaitamaRobot.modules.languages import tl

ENUM_FUNC_MAP = {
	'Types.TEXT': dispatcher.bot.send_message,
	'Types.BUTTON_TEXT': dispatcher.bot.send_message,
	'Types.STICKER': dispatcher.bot.send_sticker,
	'Types.DOCUMENT': dispatcher.bot.send_document,
	'Types.PHOTO': dispatcher.bot.send_photo,
	'Types.AUDIO': dispatcher.bot.send_audio,
	'Types.VOICE': dispatcher.bot.send_voice,
	'Types.VIDEO': dispatcher.bot.send_video
}

@run_async
@connection_status
@bot_admin
@can_promote
@user_admin
@promote_permission
@loggable
def promote(update, context):
    chat_id = update.effective_chat.id
    message = update.effective_message
    chat = update.effective_chat
    user = update.effective_user
    args = context.args
    user_id, title = extract_user_and_text(message, args)
    
    user_id = extract_user(message, args)
    if not user_id:
        message.reply_text(
            "You don't seem to be referring to a user or the ID specified is incorrect.."
        )
        return
    try:
        user_member = chat.get_member(user_id)
    except:
        return

    user_member = chat.get_member(user_id)
    if user_member.status == "administrator" or user_member.status == "creator":
        message.reply_text("This Person Is Already An Admin In This Chat")
        return ""

    if user_id == context.bot.id:
        message.reply_text("Oh , God Give Me Powers To Promote Myself 😭")
        return ""

    # set same perms as bot - bot can't assign higher perms than itself!
    bot_member = chat.get_member(context.bot.id)

    context.bot.promoteChatMember(
        chat_id,
        user_id,
        can_change_info=bot_member.can_change_info,
        can_post_messages=bot_member.can_post_messages,
        can_edit_messages=bot_member.can_edit_messages,
        can_delete_messages=bot_member.can_delete_messages,
        can_invite_users=bot_member.can_invite_users,
        can_restrict_members=bot_member.can_restrict_members,
        can_pin_messages=bot_member.can_pin_messages,
    )
    if len(title) > 16:
        message.reply_text(
            "The title length is longer than 16 characters.\nTruncating it to 16 characters."
        )
    context.bot.setChatAdministratorCustomTitle(chat.id, user_id, title)

    context.bot.sendMessage(
        chat.id,
        f"Sucessfully Promoted User <code>{user_member.user.first_name or user_id}</code> "
        f"With <code>{html.escape(title[:16])}</code> Title!",
        parse_mode=ParseMode.HTML)
    return (
        "<b>{}:</b>"
        "\n#PROMOTED"
        "\n<b>Admin:</b> {}"
        "\n<b>User:</b> {}".format(
            html.escape(chat.title),
            mention_html(user.id, user.first_name),
            mention_html(user_member.user.id, user_member.user.first_name),
        )
    )



@run_async
@connection_status
@bot_admin
@can_promote
@user_admin
@promote_permission
@loggable
def demote(update: Update, context: CallbackContext) -> str:
    bot = context.bot
    args = context.args

    chat = update.effective_chat
    message = update.effective_message
    user = update.effective_user

    user_id = extract_user(message, args)
    if not user_id:
        message.reply_text(
            "You don't seem to be referring to a user or the ID specified is incorrect.."
        )
        return

    try:
        user_member = chat.get_member(user_id)
    except:
        return
    

    if user_member.status == 'creator':
        message.reply_text(
            "This person CREATED the chat, how would I demote them?")
        return

    if not user_member.status == 'administrator':
        message.reply_text("Can't demote what wasn't promoted!")
        return

    if user_id == bot.id:
        message.reply_text(
            "I can't demote myself! Get an admin to do it for me.")
        return

    try:
        bot.promoteChatMember(
            chat.id,
            user_id,
            can_change_info=False,
            can_post_messages=False,
            can_edit_messages=False,
            can_delete_messages=False,
            can_invite_users=False,
            can_restrict_members=False,
            can_pin_messages=False,
            can_promote_members=False)

        bot.sendMessage(
            chat.id,
            f"Sucessfully demoted <b>{user_member.user.first_name or user_id}</b>!",
            parse_mode=ParseMode.HTML)

        log_message = (
            f"<b>{html.escape(chat.title)}:</b>\n"
            f"#DEMOTED\n"
            f"<b>Admin:</b> {mention_html(user.id, user.first_name)}\n"
            f"<b>User:</b> {mention_html(user_member.user.id, user_member.user.first_name)}"
        )

        return log_message
    except BadRequest:
        message.reply_text(
            "Could not demote. I might not be admin, or the admin status was appointed by another"
            " user, so I can't act upon them!")
        return


@run_async
@connection_status
@bot_admin
@can_promote
@user_admin
def set_title(update: Update, context: CallbackContext):
    bot = context.bot
    args = context.args

    chat = update.effective_chat
    message = update.effective_message

    user_id, title = extract_user_and_text(message, args)
    try:
        user_member = chat.get_member(user_id)
    except:
        return

    if not user_id:
        message.reply_text(
            "You don't seem to be referring to a user or the ID specified is incorrect.."
        )
        return

    if user_member.status == 'creator':
        message.reply_text(
            "This person CREATED the chat, how can i set custom title for him?")
        return

    if not user_member.status == 'administrator':
        message.reply_text(
            "Can't set title for non-admins!\nPromote them first to set custom title!"
        )
        return

    if user_id == bot.id:
        message.reply_text(
            "I can't set my own title myself! Get the one who made me admin to do it for me."
        )
        return

    if not title:
        message.reply_text("Setting blank title doesn't do anything!")
        return

    if len(title) > 16:
        message.reply_text(
            "The title length is longer than 16 characters.\nTruncating it to 16 characters."
        )

    try:
        bot.setChatAdministratorCustomTitle(chat.id, user_id, title)
    except BadRequest:
        message.reply_text(
            "I can't set custom title for admins that I didn't promote!")
        return

    bot.sendMessage(
        chat.id,
        f"Sucessfully set title for <code>{user_member.user.first_name or user_id}</code> "
        f"to <code>{html.escape(title[:16])}</code>!",
        parse_mode=ParseMode.HTML)


@run_async
@bot_admin
@can_pin
@user_admin
@loggable
def pin(update, context):
    user = update.effective_user  # type: Optional[User]
    message = update.effective_message
    chat = update.effective_chat  # type: Optional[Chat]
    args = context.args
    if user_can_pin(chat, user, context.bot.id) == False:
        message.reply_text("You are missing rights to pin a message!")
        return ""
    conn = connected(context.bot, update, chat, user.id, need_admin=True)
    if conn:
        chat = dispatcher.bot.getChat(conn)
        chat_id = conn
        chat_name = dispatcher.bot.getChat(conn).title
        if len(args)  <= 1:
            send_message(update.effective_message, tl(update.effective_message, "Use /pin <notify/loud/silent/violent> <link pesan>"))
            return ""
        prev_message = args[1]
        if "/" in prev_message:
            prev_message = prev_message.split("/")[-1]
    else:
        if update.effective_message.chat.type == "private":
            send_message(update.effective_message, tl(update.effective_message, "You can do this command in the group, not the PM"))
            return ""
        chat = update.effective_chat
        chat_id = update.effective_chat.id
        chat_name = update.effective_message.chat.title
        if update.effective_message.reply_to_message:
            prev_message = update.effective_message.reply_to_message.message_id
            x = update.effective_message.reply_to_message.message_id
        else:
            send_message(update.effective_message, tl(update.effective_message, "Reply to the message to pin this message to this group"))
            return ""
    is_group = chat.type != "private" and chat.type != "channel"
    is_silent = True
    if len(args) >= 1:
        is_silent = not (args[0].lower() == 'silent' or args[0].lower() == 'off' or args[0].lower() == 'mute')
    if prev_message and is_group:
        try:
            context.bot.pinChatMessage(chat.id, prev_message, disable_notification=is_silent)
            reply = f"I have pinned [this message.]({update.effective_message.link})"
            context.bot.sendMessage(chat.id, reply, parse_mode=ParseMode.MARKDOWN, quote=False)
            if conn:
                send_message(update.effective_message, tl(update.effective_message, "I've pin a message in the group {}").format(chat_name))
        except BadRequest as excp:
            if excp.message == "Chat_not_modified":
                pass
            else:
                raise
    return "<b>{}:</b>" \
      "\n#PINNED" \
      "\n<b>Admin:</b> {}".format(html.escape(chat.title), mention_html(user.id, user.first_name))


@run_async
@can_pin
@user_admin
def permapin(update, context):
	chat = update.effective_chat  # type: Optional[Chat]
	user = update.effective_user  # type: Optional[User]
	message = update.effective_message  # type: Optional[Message]
	args = context.args
	user_member = chat.get_member(user.id)
	if user_member.can_pin_messages == False:
    	    message.reply_text("You are missing the following rights to use this command:CanPinMessage!")
    	    return ""


	conn = connected(context.bot, update, chat, user.id, need_admin=False)
	if conn:
		chat = dispatcher.bot.getChat(conn)
		chat_id = conn
		chat_name = dispatcher.bot.getChat(conn).title
	else:
		if update.effective_message.chat.type == "private":
			send_message(update.effective_message(update.effective_message, "You can do this command in the group, not the PM"))
			return ""
		chat = update.effective_chat
		chat_id = update.effective_chat.id
		chat_name = update.effective_message.chat.title

	text, data_type, content, buttons = get_message_type(message)
	tombol = build_keyboard_alternate(buttons)
	try:
		message.delete()
	except BadRequest:
		pass
	if str(data_type) in ('Types.BUTTON_TEXT', 'Types.TEXT'):
		try:
			sendingmsg = context.bot.send_message(chat_id, text, parse_mode="markdown",
								 disable_web_page_preview=True, reply_markup=InlineKeyboardMarkup(tombol))
		except BadRequest:
			context.bot.send_message(chat_id(update.effective_message, "Incorrect markdown text!\nIf you don't know what markdown is, please type `/markdownhelp` on PM."), parse_mode="markdown")
			return
	else:
		sendingmsg = ENUM_FUNC_MAP[str(data_type)](chat_id, content, caption=text, parse_mode="markdown", disable_web_page_preview=True, reply_markup=InlineKeyboardMarkup(tombol))
	try:
		context.bot.pinChatMessage(chat_id, sendingmsg.message_id)
	except BadRequest:
		send_message(update.effective_message(update.effective_message, "I don't have access to message pins!"))


@run_async
@can_pin
@user_admin
def permanent_pin_set(update, context):
	user = update.effective_user  # type: Optional[User]
	chat = update.effective_chat  # type: Optional[Chat]
	args = context.args
	user_member = chat.get_member(user.id)
	if user_member.can_pin_messages == False:
    	    message.reply_text("You are missing the following rights to use this command:CanPinMessage!")
    	    return ""


	conn = connected(context.bot, update, chat, user.id, need_admin=True)
	if conn:
		chat = dispatcher.bot.getChat(conn)
		chat_id = conn
		chat_name = dispatcher.bot.getChat(conn).title
		if not args:
			get_permapin = sql.get_permapin(chat_id)
			text_maker = (update.effective_message, "The permanent pin is currently set: `{}`").format(bool(int(get_permapin)))
			if get_permapin:
				if chat.username:
					old_pin = "https://t.me/{}/{}".format(chat.username, get_permapin)
				else:
					old_pin = "https://t.me/c/{}/{}".format(str(chat.id)[4:], get_permapin)
				text_maker += (update.effective_message, "\nTo permanently disable the pin: `/permanentpin off`")
				text_maker += (update.effective_message, "\n\n[The message permanent pin is here]({})").format(old_pin)
			send_message(update.effective_message, (update.effective_message, text_maker), parse_mode="markdown")
			return ""
		prev_message = args[0]
		if prev_message == "off":
			sql.set_permapin(chat_id, 0)
			send_message(update.effective_message, (update.effective_message, "The pin has been permanently disabled!"))
			return
		if "/" in prev_message:
			prev_message = prev_message.split("/")[-1]
	else:
		if update.effective_message.chat.type == "private":
			send_message(update.effective_message, (update.effective_message, "You can do this command in the group, not the PM"))
			return ""
		chat = update.effective_chat
		chat_id = update.effective_chat.id
		chat_name = update.effective_message.chat.title
		if update.effective_message.reply_to_message:
			prev_message = update.effective_message.reply_to_message.message_id
		elif len(args) >= 1 and args[0] == "off":
			sql.set_permapin(chat.id, 0)
			send_message(update.effective_message(update.effective_message, "The pin has been permanently disabled!"))
			return
		else:
			get_permapin = sql.get_permapin(chat_id)
			text_maker = (update.effective_message, "The permanent pin is currently set: `{}`").format(bool(int(get_permapin)))
			if get_permapin:
				if chat.username:
					old_pin = "https://t.me/{}/{}".format(chat.username, get_permapin)
				else:
					old_pin = "https://t.me/c/{}/{}".format(str(chat.id)[4:], get_permapin)
				text_maker += (update.effective_message, "\nTo permanently disable the pin: `/permanentpin off`")
				text_maker += (update.effective_message, "\n\n[The message permanent pin is here]({})").format(old_pin)
			send_message(update.effective_message, text_maker, parse_mode="markdown")
			return ""

	is_group = chat.type != "private" and chat.type != "channel"

	if prev_message and is_group:
		sql.set_permapin(chat.id, prev_message)
		send_message(update.effective_message, (update.effective_message, "Permanent pin successfully set!"))
		return "<b>{}:</b>" \
			   "\n#PERMANENT_PIN" \
			   "\n<b>Admin:</b> {}".format(html.escape(chat.title), mention_html(user.id, user.first_name))

	return ""


@run_async
def permanent_pin(update, context):
	user = update.effective_user  # type: Optional[User]
	chat = update.effective_chat  # type: Optional[Chat]
	message = update.effective_message
	args = context.args
	user_member = chat.get_member(user.id)
	if user_member.can_pin_messages == False:
    	    message.reply_text("You are missing the following rights to use this command:CanPinMessage!")
    	    return ""


	get_permapin = sql.get_permapin(chat.id)
	if get_permapin and not user.id == context.bot.id:
		try:
			to_del = context.bot.pinChatMessage(chat.id, get_permapin, disable_notification=True)
		except BadRequest:
			sql.set_permapin(chat.id, 0)
			if chat.username:
				old_pin = "https://t.me/{}/{}".format(chat.username, get_permapin)
			else:
				old_pin = "https://t.me/c/{}/{}".format(str(chat.id)[4:], get_permapin)
			send_message(update.effective_message(update.effective_message, "*Permanent pin error: * \nI can't pin messages here! \nMake sure I'm admin and can pin messages. \n \nPermanent pins are disabled, [message permanent old pin is here]({})").format(old_pin), parse_mode="markdown")
			return

		if to_del:
			try:
				context.bot.deleteMessage(chat.id, message.message_id+1)
			except BadRequest:
				print("Permanent pin error: cannot delete pin msg")
	


@run_async
@user_admin
def refresh_admin(update, _):
    try:
        ADMIN_CACHE.pop(update.effective_chat.id)
    except KeyError:
        pass

    update.effective_message.reply_text("Admins cache refreshed!")


@run_async
@bot_admin
@can_pin
@user_admin
@loggable
def unpin(update: Update, context: CallbackContext) -> str:
    bot = context.bot
    chat = update.effective_chat
    user = update.effective_user

    try:
        bot.unpinChatMessage(chat.id)
    except BadRequest as excp:
        if excp.message == "Chat_not_modified":
            pass
        else:
            raise

    log_message = (
        f"<b>{html.escape(chat.title)}:</b>\n"
        f"#UNPINNED\n"
        f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}")

    return log_message


            

@run_async
@bot_admin
@user_admin
@connection_status
def invite(update: Update, context: CallbackContext):
    bot = context.bot
    chat = update.effective_chat

    if chat.username:
        update.effective_message.reply_text(f"https://t.me/{chat.username}")
    elif chat.type == chat.SUPERGROUP or chat.type == chat.CHANNEL:
        bot_member = chat.get_member(bot.id)
        if bot_member.can_invite_users:
            invitelink = bot.exportChatInviteLink(chat.id)
            update.effective_message.reply_text(invitelink)
        else:
            update.effective_message.reply_text(
                "I don't have access to the invite link, try changing my permissions!"
            )
    else:
        update.effective_message.reply_text(
            "I can only give you invite links for supergroups and channels, sorry!"
        )


@run_async
@connection_status
def adminlist(update, context):
    chat = update.effective_chat  # type: Optional[Chat]
    user = update.effective_user  # type: Optional[User]
    args = context.args
    bot = context.bot

    if update.effective_message.chat.type == "private":
        send_message(update.effective_message,
                     "This command only works in Groups.")
        return

    chat = update.effective_chat
    chat_id = update.effective_chat.id
    chat_name = update.effective_message.chat.title

    try:
        msg = update.effective_message.reply_text(
            'Fetching group admins...', parse_mode=ParseMode.MARKDOWN)
    except BadRequest:
        msg = update.effective_message.reply_text(
            'Fetching group admins...',
            quote=False,
            parse_mode=ParseMode.MARKDOWN)

    administrators = bot.getChatAdministrators(chat_id)
    text = "Admins in *{}*:".format(update.effective_chat.title)

    bot_admin_list = []

    for admin in administrators:
        user = admin.user
        status = admin.status
        custom_title = admin.custom_title

        if user.first_name == '':
            name = "☠ Deleted Account"
        else:
            name = "{}".format(
                mention_markdown(user.id, user.first_name + " " +
                                 (user.last_name or "")))

        if user.is_bot:
            bot_admin_list.append(name)
            administrators.remove(admin)
            continue

        #if user.username:
        #    name = escape_markdown("@" + user.username)
        if status == "creator":
            text += "\n 👑 Creator:"
            text += "\n` • `{}\n".format(name)

            if custom_title:
                text += f"┗━ `{escape_markdown(custom_title)}`\n"

    text += "\n🔱 Admins:"

    custom_admin_list = {}
    normal_admin_list = []

    for admin in administrators:
        user = admin.user
        status = admin.status
        custom_title = admin.custom_title

        if user.first_name == '':
            name = "☠ Deleted Account"
        else:
            name = "{}".format(
                mention_markdown(user.id, user.first_name + " " +
                                 (user.last_name or "")))
        #if user.username:
        #    name = escape_markdown("@" + user.username)
        if status == "administrator":
            if custom_title:
                try:
                    custom_admin_list[custom_title].append(name)
                except KeyError:
                    custom_admin_list.update({custom_title: [name]})
            else:
                normal_admin_list.append(name)

    for admin in normal_admin_list:
        text += "\n` • `{}".format(admin)

    for admin_group in custom_admin_list.copy():
        if len(custom_admin_list[admin_group]) == 1:
            text += "\n` • `{} | `{}`".format(custom_admin_list[admin_group][0],
                                              escape_markdown(admin_group))
            custom_admin_list.pop(admin_group)

    text += "\n"
    for admin_group in custom_admin_list:
        text += "\n🔘 `{}`".format(admin_group)
        for admin in custom_admin_list[admin_group]:
            text += "\n` • `{}".format(admin)
        text += "\n"

    text += "\n🤖 Bots:"
    for each_bot in bot_admin_list:
        text += "\n` • `{}".format(each_bot)

    try:
        msg.edit_text(text, parse_mode=ParseMode.MARKDOWN)
    except BadRequest:  # if original message is deleted
        return

@run_async
@connection_status
def adminslist(update: Update, context: CallbackContext):
    bot = context.bot
    chat = update.effective_chat
    user = update.effective_user

    chat_id = chat.id
    update_chat_title = chat.title
    message_chat_title = update.effective_message.chat.title

    administrators = bot.getChatAdministrators(chat_id)

    if update_chat_title == message_chat_title:
        chat_name = "this chat"
    else:
        chat_name = update_chat_title

    text = f"Admins in *{chat_name}*:"

    for admin in administrators:
        user = admin.user
        name = f"[{user.first_name + (user.last_name or '')}](tg://user?id={user.id})"
        text += f"\n - {name}"

    update.effective_message.reply_text(text, parse_mode=ParseMode.MARKDOWN)

def __chat_settings__(chat_id, user_id):
    return "You are *admin*: `{}`".format(
        dispatcher.bot.get_chat_member(chat_id, user_id).status in (
            "administrator", "creator"))


__help__ = """
 • `/admins`*:* list of admins in the chat
 • `adminlist`*:* List of admins in chat

*Admins only:*
 • `/pin`*:* silently pins the message replied to - add `'loud'` or `'notify'` to give notifs to users.
 • `/unpin`*:* unpins the currently pinned message
 • `/permapin`*:* <text>: Pin a custom message through the bot. This message can contain markdown, buttons, and all the other cool features.
 • `/invitelink`*:* gets invitelink
 • `/promote`*:* <title> promotes the user replied to with custom title
 • `/admincache`*:* force refresh the admins list
 • `/tagall` *:* Tag Everyone in Chat
 • `/cleandeleted`*:* Removed Deleted Accounts In Chat
 • `/cleaninactive`*:* Clean All Inactive Members
 • `/demote`*:* demotes the user replied to
 • `/title <title here>`*:* sets a custom title for an admin that the bot promoted


Sometimes, you promote or demote an admin manually, and Anie doesn't realise it immediately. This is because to avoid spamming telegram servers, admin status is cached locally.
This means that you sometimes have to wait a few minutes for admin rights to update. If you want to update them immediately, you can use the /admincache command; that'll force Anie to check who the admins are again.
"""

ADMINLIST_HANDLER = DisableAbleCommandHandler("disabledt", adminlist)
ADMINSLIST_HANDLER = DisableAbleCommandHandler("adminlist", adminslist)

PIN_HANDLER = CommandHandler("pin", pin, filters=Filters.group)
UNPIN_HANDLER = CommandHandler("unpin", unpin, filters=Filters.group)
PERMAPIN_HANDLER = CommandHandler("permapin", permapin, filters=Filters.group)

INVITE_HANDLER = DisableAbleCommandHandler("invitelink", invite)

PROMOTE_HANDLER = DisableAbleCommandHandler("promote", promote)
DEMOTE_HANDLER = DisableAbleCommandHandler("demote", demote)
PERMANENT_PIN_SET_HANDLER = CommandHandler("permanentpin", permanent_pin_set, pass_args=True, filters=Filters.group)
PERMANENT_PIN_HANDLER = MessageHandler(Filters.status_update.pinned_message | Filters.user(777000), permanent_pin)

ADMIN_REFRESH_HANDLER = CommandHandler(
    "admincache", refresh_admin, filters=Filters.group)

SET_TITLE_HANDLER = CommandHandler("title", set_title)
#FED_ADMIN_HANDLER = CommandHandler("fedadmin", fed_admin)
dispatcher.add_handler(ADMINLIST_HANDLER)
dispatcher.add_handler(ADMINSLIST_HANDLER)
dispatcher.add_handler(PIN_HANDLER)
dispatcher.add_handler(PERMAPIN_HANDLER)
dispatcher.add_handler(UNPIN_HANDLER)
dispatcher.add_handler(INVITE_HANDLER)
dispatcher.add_handler(PROMOTE_HANDLER)
dispatcher.add_handler(PERMANENT_PIN_SET_HANDLER)
dispatcher.add_handler(PERMANENT_PIN_HANDLER)
#dispatcher.add_handler(XPROMOTE_HANDLER)
dispatcher.add_handler(DEMOTE_HANDLER)
dispatcher.add_handler(SET_TITLE_HANDLER)
#dispatcher.add_handler(FED_ADMIN_HANDLER)
dispatcher.add_handler(ADMIN_REFRESH_HANDLER)

__mod_name__ = "Admin"
__command_list__ = ["adminlist", "admins", "invitelink", "promote", "demote"]
__handlers__ = [
    ADMINLIST_HANDLER, ADMINSLIST_HANDLER, PIN_HANDLER, UNPIN_HANDLER, INVITE_HANDLER,
    PROMOTE_HANDLER, DEMOTE_HANDLER, SET_TITLE_HANDLER
]
