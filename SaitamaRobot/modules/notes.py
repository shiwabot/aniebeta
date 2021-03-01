import re, ast
from io import BytesIO
from typing import Optional
from telegram import Message, Update, Bot
import SaitamaRobot.modules.sql.notes_sql as sql
from SaitamaRobot import LOGGER, JOIN_LOGGER, SUPPORT_CHAT, dispatcher
from SaitamaRobot.modules.disable import DisableAbleCommandHandler
from SaitamaRobot.modules.helper_funcs.chat_status import user_admin, connection_status, user_admin_no_reply, user_can_change, bot_admin
from SaitamaRobot.modules.helper_funcs.misc import (build_keyboard,
                                                    revert_buttons, build_keyboard_parser)
from SaitamaRobot.modules.helper_funcs.msg_types import get_note_type
from SaitamaRobot.modules.helper_funcs.string_handling import escape_invalid_curly_brackets
from telegram import (MAX_MESSAGE_LENGTH, InlineKeyboardMarkup, Message,
                      ParseMode, Update, InlineKeyboardButton)
from telegram.error import BadRequest
from telegram.utils.helpers import escape_markdown, mention_markdown
from telegram.ext import (CallbackContext, CommandHandler, Filters,
                          MessageHandler, CallbackQueryHandler)
from telegram.ext.dispatcher import run_async
from SaitamaRobot.modules.connection import connected
from SaitamaRobot.modules.languages import tl
from SaitamaRobot.modules.helper_funcs.alternate import send_message, send_message_raw

FILE_MATCHER = re.compile(r"^###file_id(!photo)?###:(.*?)(?:\s|$)")
STICKER_MATCHER = re.compile(r"^###sticker(!photo)?###:")
BUTTON_MATCHER = re.compile(r"^###button(!photo)?###:(.*?)(?:\s|$)")
MYFILE_MATCHER = re.compile(r"^###file(!photo)?###:")
MYPHOTO_MATCHER = re.compile(r"^###photo(!photo)?###:")
MYAUDIO_MATCHER = re.compile(r"^###audio(!photo)?###:")
MYVOICE_MATCHER = re.compile(r"^###voice(!photo)?###:")
MYVIDEO_MATCHER = re.compile(r"^###video(!photo)?###:")
MYVIDEONOTE_MATCHER = re.compile(r"^###video_note(!photo)?###:")

ENUM_FUNC_MAP = {
    sql.Types.TEXT.value: dispatcher.bot.send_message,
    sql.Types.BUTTON_TEXT.value: dispatcher.bot.send_message,
    sql.Types.STICKER.value: dispatcher.bot.send_sticker,
    sql.Types.DOCUMENT.value: dispatcher.bot.send_document,
    sql.Types.PHOTO.value: dispatcher.bot.send_photo,
    sql.Types.AUDIO.value: dispatcher.bot.send_audio,
    sql.Types.VOICE.value: dispatcher.bot.send_voice,
    sql.Types.VIDEO.value: dispatcher.bot.send_video
}


# Do not async
#@connection_status 
def get(update, context, notename, show_none=True, no_format=False):
	bot = context.bot
	chat = update.effective_chat  # type: Optional[Chat]
	user = update.effective_user  # type: Optional[User]
	conn = connected(bot, update, chat, user.id, need_admin=False)
	if conn:
		chat_id = conn
		send_id = user.id
	else:
		chat_id = update.effective_chat.id
		send_id = chat_id

	note = sql.get_note(chat_id, notename)
	message = update.effective_message  # type: Optional[Message]

	if note:
		# If we're replying to a message, reply to that message (unless it's an error)
		if message.reply_to_message:
			reply_id = message.reply_to_message.message_id
		else:
			reply_id = message.message_id

		if note.is_reply:
			if MESSAGE_DUMP:
				try:
					bot.forward_message(chat_id=chat_id, from_chat_id=MESSAGE_DUMP, message_id=note.value)
				except BadRequest as excp:
					if excp.message == "Message to forward not found":
						send_message(update.effective_message, tl(update.effective_message, "This message appears to have disappeared - I will delete it "
										   "from your note list."))
						sql.rm_note(chat_id, notename)
					else:
						raise
			else:
				try:
					bot.forward_message(chat_id=chat_id, from_chat_id=chat_id, message_id=note.value)
				except BadRequest as excp:
					if excp.message == "Message to forward not found":
						send_message(update.effective_message, tl(update.effective_message, "It looks like the original sender of this note has been deleted "
										   "their message - sorry! Get your bot admin to start using "
										   "dump messages to avoid this. I will delete this note from "
										   "your saved note."))
						sql.rm_note(chat_id, notename)
					else:
						raise
		else:

			VALID_WELCOME_FORMATTERS = ['first', 'last', 'fullname', 'username', 'id', 'chatname', 'mention', 'rules']
			valid_format = escape_invalid_curly_brackets(note.value, VALID_WELCOME_FORMATTERS)
			if valid_format:
				text = valid_format.format(first=escape_markdown(message.from_user.first_name),
											  last=escape_markdown(message.from_user.last_name or message.from_user.first_name),
											  fullname=escape_markdown(" ".join([message.from_user.first_name, message.from_user.last_name] if message.from_user.last_name else [message.from_user.first_name])), username="@" + message.from_user.username if message.from_user.username else mention_markdown(message.from_user.id, message.from_user.first_name), mention=mention_markdown(message.from_user.id, message.from_user.first_name), chatname=escape_markdown(message.chat.title if message.chat.type != "private" else message.from_user.first_name), id=message.from_user.id, rules="http://t.me/{}?start={}".format(bot.username, chat_id))
			else:
				text = ""

			keyb = []
			parseMode = ParseMode.MARKDOWN
			buttons = sql.get_buttons(chat_id, notename)
			if no_format:
				parseMode = None
				text += revert_buttons(buttons)
			else:
				keyb = build_keyboard_parser(bot, chat_id, buttons)

			keyboard = InlineKeyboardMarkup(keyb)

			try:
				is_private, is_delete = sql.get_private_note(chat.id)
				
				if note.msgtype in (sql.Types.BUTTON_TEXT, sql.Types.TEXT):
					try:
						if is_delete:
							update.effective_message.delete()
							
						if is_private:
							bot.send_message(user.id, text,
										 parse_mode=parseMode, disable_web_page_preview=True,
										 reply_markup=keyboard)
							update.effective_message.reply_text("Note has been sent to PM! Kindly Check.!")
						else:
							bot.send_message(send_id, text, reply_to_message_id=reply_id,
										 parse_mode=parseMode, disable_web_page_preview=True,
										 reply_markup=keyboard)
					except BadRequest as excp:
						if excp.message == "Wrong http url":
							failtext = tl(update.effective_message, "Error: The URL on the button is invalid! Please update this note.")
							failtext += "\n\n```\n{}```".format(note.value + revert_buttons(buttons))
							send_message(update.effective_message, failtext, parse_mode="markdown")
						elif excp.message == "Button_url_invalid":
							failtext = tl(update.effective_message, "Error: The URL on the button is invalid! Please update this note.")
							failtext += "\n\n```\n{}```".format(note.value + revert_buttons(buttons))
							send_message(update.effective_message, failtext, parse_mode="markdown")
						elif excp.message == "Message can't be deleted":
							pass
						elif excp.message == "Have no rights to send a message":
							pass
					except Unauthorized as excp:
						update.effective_message.reply_text("Note has been sent to PM! Kindly Check.")
						pass
				else:
					try:
						if is_delete:
							update.effective_message.delete()
						if is_private:
							ENUM_FUNC_MAP[note.msgtype](user.id, note.file, caption=text, parse_mode=parseMode, disable_web_page_preview=True, reply_markup=keyboard)
						else:
							ENUM_FUNC_MAP[note.msgtype](send_id, note.file, caption=text, reply_to_message_id=reply_id, parse_mode=parseMode, disable_web_page_preview=True, reply_markup=keyboard)
					except BadRequest as excp:
						if excp.message == "Message can't be deleted":
							pass
						elif excp.message == "Have no rights to send a message":
							pass
					except Unauthorized as excp:
						update.effective_message.reply_text("Note has been sent to PM! Kindly Check.!")
						pass
					
			except BadRequest as excp:
				if excp.message == "Entity_mention_user_invalid":
					send_message(update.effective_message, tl(update.effective_message, "Looks like you're trying to mention someone that I've never seen before. "
									   "If you really want to mention it, forward one of their messages to me, "
									   "and I will be able to tag them!"))
				elif FILE_MATCHER.match(note.value):
					send_message(update.effective_message, tl(update.effective_message, "Note this is the wrong file imported from another bot - I can't use it "
									   "this. If you really need it, you should save it again. "
									   "In the meantime, I will delete it from your record list."))
					sql.rm_note(chat_id, notename)
				else:
					send_message(update.effective_message, tl(update.effective_message, "This note cannot be sent because it is in the wrong format."))
					LOGGER.exception("Tidak dapat menguraikan pesan #%s di obrolan %s", notename, str(chat_id))
					LOGGER.warning("Pesan itu: %s", str(note.value))
		return
	elif show_none:
		send_message(update.effective_message, tl(update.effective_message, "This note does not exist"))


@run_async
@connection_status
def cmd_get(update: Update, context: CallbackContext):
    bot, args = context.bot, context.args
    if len(args) >= 2 and args[1].lower() == "noformat":
        get(update, context, args[0].lower(), show_none=True, no_format=True)
    elif len(args) >= 1:
        get(update, context, args[0].lower(), show_none=True)
    else:
        update.effective_message.reply_text("Get rekt")


@run_async
@connection_status
def hash_get(update: Update, context: CallbackContext):
    message = update.effective_message.text
    fst_word = message.split()[0]
    no_hash = fst_word[1:].lower()
    get(update, context, no_hash, show_none=False)


@run_async
@connection_status
def slash_get(update: Update, context: CallbackContext):
    message, chat_id = update.effective_message.text, update.effective_chat.id
    no_slash = message[1:]
    note_list = sql.get_all_chat_notes(chat_id)

    try:
        noteid = note_list[int(no_slash) - 1]
        note_name = str(noteid).strip(">").split()[1]
        get(update, context, note_name, show_none=False)
    except IndexError:
        update.effective_message.reply_text("Wrong Note ID 😾")


@connection_status
@run_async
@bot_admin
@user_admin
@user_can_change
def save(update, context):
	chat = update.effective_chat  # type: Optional[Chat]
	user = update.effective_user  # type: Optional[User]
	conn = connected(context.bot, update, chat, user.id)
	if conn:
		chat_id = conn
		chat_name = dispatcher.bot.getChat(conn).title
	else:
		chat_id = update.effective_chat.id
		if chat.type == "private":
			chat_name = "local note"
		else:
			chat_name = chat.title

	msg = update.effective_message  # type: Optional[Message]

	checktext = msg.text.split()
	if msg.reply_to_message:
		if len(checktext) <= 1:
			msg.reply_text("You must provide a name for this note!")
			return
	else:
		if len(checktext) <= 2:
			msg.reply_text("You must provide a name for this note!")
			return

	note_name, text, data_type, content, buttons = get_note_type(msg)
	note_name = note_name.lower()

	if data_type is None:
		msg.reply_text("You must provide a name for this note for more use help!")
		return

	if len(text.strip()) == 0:
		text = "`" + note_name + "`"

	sql.add_note_to_db(chat_id, note_name, text, data_type, buttons=buttons, file=content)
	if conn:
		savedtext = (update.effective_message, "Ok, note `{note_name}` save in *{chat_name}*.").format(note_name=note_name, chat_name=chat_name)
	else:
		msg.reply_text("Saved, note `{note_name}`".format(note_name=note_name), parse_mode=ParseMode.MARKDOWN)
	try:
		send_message(update.effective_message, parse_mode=ParseMode.MARKDOWN)
	except BadRequest:
		if conn:
			savedtext = (update.effective_message, "Your, a note <code>{note_name}</code> save in <b>{chat_name}</b>.").format(note_name=note_name, chat_name=chat_name)
		else:
			savedtext = (update.effective_message, "Your, a note <code>{note_name}</code> Saved.").format(note_name=note_name)
		send_message(update.effective_message, savedtext, parse_mode=ParseMode.HTML)


@run_async
@user_admin
@user_can_change
@connection_status
def clear(update: Update, context: CallbackContext):
    args = context.args
    chat = update.effective_chat
    chat_id = update.effective_chat.id
    message = update.effective_message  # type: Optional[Message]
    user = update.effective_user
    user_member = chat.get_member(user.id)
    if user_member.can_change_info == False:	
    	    message.reply_text("You don't have permission to do this!")
    	    return

    if len(args) >= 1:
        notename = args[0].lower()

        if sql.rm_note(chat_id, notename):
            update.effective_message.reply_text("Successfully removed note.")
        else:
            update.effective_message.reply_text(
                "That's not a note in my database!")

@run_async
#@spamcheck
@user_admin
@user_can_change
def private_note(update, context):
	args = context.args
	chat = update.effective_chat  # type: Optional[Chat]
	user = update.effective_user  # type: Optional[User]
	conn = connected(context.bot, update, chat, user.id)
	if conn:
		chat_id = conn
		chat_name = dispatcher.bot.getChat(conn).title
	else:
		chat_id = update.effective_chat.id
		if chat.type == "private":
			chat_name = chat.title
		else:
			chat_name = chat.title

	if len(args) >= 1:
		if args[0] in ("yes", "on", "ya"):
			if len(args) >= 2:
				if args[1] == "del":
					sql.private_note(str(chat_id), True, True)
					send_message(update.effective_message, tl(update.effective_message, "Private Note is *activated*, when a user retrieves a note, a note message will be sent to the PM and the user's message will be immediately deleted."), parse_mode="markdown")
				else:
					sql.private_note(str(chat_id), True, False)
					send_message(update.effective_message, tl(update.effective_message, "Private Note is *activated*, when a user retrieves a note, a note message will be sent to the PM."), parse_mode="markdown")
			else:
				sql.private_note(str(chat_id), True, False)
				send_message(update.effective_message, tl(update.effective_message, "Private Note is *activated*, when a user retrieves a note, a note message will be sent to the PM."), parse_mode="markdown")
		elif args[0] in ("no", "off"):
			sql.private_note(str(chat_id), False, False)
			send_message(update.effective_message, tl(update.effective_message, "Private Note is *deactivated*, note messages will be sent to the group."), parse_mode="markdown")
		else:
			send_message(update.effective_message, tl(update.effective_message, "Unknown argument - please use 'yes', or 'no'."))
	else:
		is_private, is_delete = sql.get_private_note(chat_id)
		print(is_private, is_delete)
		send_message(update.effective_message, tl(update.effective_message, "Private Note settings in {}: *{}*{}").format(chat_name, "Enabled" if is_private else "Disabled", " - *Hash will be deleted*" if is_delete else ""), parse_mode="markdown")


@run_async
@connection_status
def list_notes(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    note_list = sql.get_all_chat_notes(chat_id)
    notes = len(note_list) + 1
    msg = "Get note by `/notenumber` or `#notename` \n\n  *ID*    *Note* \n"
    for note_id, note in zip(range(1, notes), note_list):
        if note_id < 10:
            note_name = f"`{note_id:2}.`  `#{(note.name.lower())}`\n"
        else:
            note_name = f"`{note_id}.`  `#{(note.name.lower())}`\n"
        if len(msg) + len(note_name) > MAX_MESSAGE_LENGTH:
            update.effective_message.reply_text(
                msg, parse_mode=ParseMode.MARKDOWN)
            msg = ""
        msg += note_name

    if not note_list:
        update.effective_message.reply_text("No notes in this chat!")

    elif len(msg) != 0:
        update.effective_message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)

@run_async
@user_admin
def clear_notes(update, context):
    chat = update.effective_chat
    user = update.effective_user
    msg = update.effective_message

    chatmem = chat.get_member(user.id)
    if chatmem.status == "creator":
        allnotes = sql.get_all_chat_notes(chat.id)
        if not allnotes:
            msg.reply_text("No notes saved here what should i delete?")
            return
        else:
            msg.reply_text(
                "Do you really wanna delete all of the notes??",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="Yes I'm sure️", callback_data="rmnotes_true"
                            )
                        ],
                        [
                            InlineKeyboardButton(
                                text="Cancel", callback_data="rmnotes_cancel"
                            )
                        ],
                    ]
                ),
            )

    else:
        msg.reply_text("This command can be only used by chat OWNER!")


@run_async
@user_admin_no_reply
def rmbutton(update, context):
    query = update.callback_query
    userid = update.effective_user.id
    match = query.data.split("_")[1]
    chat = update.effective_chat

    usermem = chat.get_member(userid).status

    if match == "cancel" and usermem == "creator":
        return query.message.edit_text("Cancelled deletion of notes.")

    elif match == "true" and usermem == "creator":

        allnotes = sql.get_all_chat_notes(chat.id)
        count = 0
        notelist = []
        for notename in allnotes:
            count += 1
            note = notename.name.lower()
            notelist.append(note)

        for i in notelist:
            sql.rm_note(chat.id, i)
        query.message.edit_text(f"Successfully cleaned {count} notes in {chat.title}.")


def __import_data__(chat_id, data):
    failures = []
    for notename, notedata in data.get("extra", {}).items():
        match = FILE_MATCHER.match(notedata)
        matchsticker = STICKER_MATCHER.match(notedata)
        matchbtn = BUTTON_MATCHER.match(notedata)
        matchfile = MYFILE_MATCHER.match(notedata)
        matchphoto = MYPHOTO_MATCHER.match(notedata)
        matchaudio = MYAUDIO_MATCHER.match(notedata)
        matchvoice = MYVOICE_MATCHER.match(notedata)
        matchvideo = MYVIDEO_MATCHER.match(notedata)
        matchvn = MYVIDEONOTE_MATCHER.match(notedata)

        if match:
            failures.append(notename)
            notedata = notedata[match.end():].strip()
            if notedata:
                sql.add_note_to_db(chat_id, notename[1:], notedata,
                                   sql.Types.TEXT)
        elif matchsticker:
            content = notedata[matchsticker.end():].strip()
            if content:
                sql.add_note_to_db(
                    chat_id,
                    notename[1:],
                    notedata,
                    sql.Types.STICKER,
                    file=content)
        elif matchbtn:
            parse = notedata[matchbtn.end():].strip()
            notedata = parse.split("<###button###>")[0]
            buttons = parse.split("<###button###>")[1]
            buttons = ast.literal_eval(buttons)
            if buttons:
                sql.add_note_to_db(
                    chat_id,
                    notename[1:],
                    notedata,
                    sql.Types.BUTTON_TEXT,
                    buttons=buttons,
                )
        elif matchfile:
            file = notedata[matchfile.end():].strip()
            file = file.split("<###TYPESPLIT###>")
            notedata = file[1]
            content = file[0]
            if content:
                sql.add_note_to_db(
                    chat_id,
                    notename[1:],
                    notedata,
                    sql.Types.DOCUMENT,
                    file=content)
        elif matchphoto:
            photo = notedata[matchphoto.end():].strip()
            photo = photo.split("<###TYPESPLIT###>")
            notedata = photo[1]
            content = photo[0]
            if content:
                sql.add_note_to_db(
                    chat_id,
                    notename[1:],
                    notedata,
                    sql.Types.PHOTO,
                    file=content)
        elif matchaudio:
            audio = notedata[matchaudio.end():].strip()
            audio = audio.split("<###TYPESPLIT###>")
            notedata = audio[1]
            content = audio[0]
            if content:
                sql.add_note_to_db(
                    chat_id,
                    notename[1:],
                    notedata,
                    sql.Types.AUDIO,
                    file=content)
        elif matchvoice:
            voice = notedata[matchvoice.end():].strip()
            voice = voice.split("<###TYPESPLIT###>")
            notedata = voice[1]
            content = voice[0]
            if content:
                sql.add_note_to_db(
                    chat_id,
                    notename[1:],
                    notedata,
                    sql.Types.VOICE,
                    file=content)
        elif matchvideo:
            video = notedata[matchvideo.end():].strip()
            video = video.split("<###TYPESPLIT###>")
            notedata = video[1]
            content = video[0]
            if content:
                sql.add_note_to_db(
                    chat_id,
                    notename[1:],
                    notedata,
                    sql.Types.VIDEO,
                    file=content)
        elif matchvn:
            video_note = notedata[matchvn.end():].strip()
            video_note = video_note.split("<###TYPESPLIT###>")
            notedata = video_note[1]
            content = video_note[0]
            if content:
                sql.add_note_to_db(
                    chat_id,
                    notename[1:],
                    notedata,
                    sql.Types.VIDEO_NOTE,
                    file=content)
        else:
            sql.add_note_to_db(chat_id, notename[1:], notedata, sql.Types.TEXT)

    if failures:
        with BytesIO(str.encode("\n".join(failures))) as output:
            output.name = "failed_imports.txt"
            dispatcher.bot.send_document(
                chat_id,
                document=output,
                filename="failed_imports.txt",
                caption="These files/photos failed to import due to originating "
                "from another bot. This is a telegram API restriction, and can't "
                "be avoided. Sorry for the inconvenience!",
            )


def __stats__():
    return f"• {sql.num_notes()} notes, across {sql.num_chats()} chats."


def __migrate__(old_chat_id, new_chat_id):
    sql.migrate_chat(old_chat_id, new_chat_id)


def __chat_settings__(chat_id, user_id):
    notes = sql.get_all_chat_notes(chat_id)
    return f"There are `{len(notes)}` notes in this chat."


__help__ = """
 • `/get <notename>`*:* get the note with this notename
 • `#<notename>`*:* same as /get
 • `/notes` or `/saved`*:* list all saved notes in this chat
 • `/number` *:* Will pull the note of that number in the list. 
If you would like to retrieve the contents of a note without any formatting, use `/get <notename> noformat`. This can \
be useful when updating a current note.

*Admins only:*
 • `/save <notename> <notedata>`*:* saves notedata as a note with name notename
A button can be added to a note by using standard markdown link syntax - the link should just be prepended with a \
`buttonurl:` section, as such: `[somelink](buttonurl:example.com)`. Check `/markdownhelp` for more info.
 • `/save <notename>`*:* save the replied message as a note with name notename
 • `/privatenote on` / `off` allow bot to send group message to users pm
 • `/clear <notename>`*:* clear note with this name
 • `/clearallnotes` Remove all notes at once [Chat Owner Only]
 *Note:* Note names are case-insensitive, and they are automatically converted to lowercase before getting saved.
"""

__mod_name__ = "Notes"

GET_HANDLER = CommandHandler("get", cmd_get)
HASH_GET_HANDLER = MessageHandler(Filters.regex(r"^#[^\s]+"), hash_get)
SLASH_GET_HANDLER = MessageHandler(Filters.regex(r"^/\d+$"), slash_get)
SAVE_HANDLER = CommandHandler("save", save)
DELETE_HANDLER = CommandHandler("clear", clear)
CLEARALLNOTES_HANDLER = CommandHandler("clearallnotes", clear_notes, filters=Filters.group)
PMNOTE_HANDLER = CommandHandler("privatenote", private_note, pass_args=True)

RMBTN_HANDLER = CallbackQueryHandler(rmbutton, pattern=r"rmnotes_")

LIST_HANDLER = DisableAbleCommandHandler(["notes", "saved"],
                                         list_notes,
                                         admin_ok=True)

dispatcher.add_handler(GET_HANDLER)
dispatcher.add_handler(SAVE_HANDLER)
dispatcher.add_handler(LIST_HANDLER)
dispatcher.add_handler(DELETE_HANDLER)
dispatcher.add_handler(HASH_GET_HANDLER)
dispatcher.add_handler(SLASH_GET_HANDLER)
dispatcher.add_handler(CLEARALLNOTES_HANDLER)
dispatcher.add_handler(RMBTN_HANDLER)
dispatcher.add_handler(PMNOTE_HANDLER)
