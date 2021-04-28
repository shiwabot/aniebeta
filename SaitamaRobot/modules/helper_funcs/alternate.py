from telegram.error import BadRequest
from functools import wraps
from telegram import error, ChatAction
from SaitamaRobot import dispatcher

def send_message(message, text, *args, **kwargs):
    try:
        return message.reply_text(text, *args, **kwargs)
    except BadRequest as err:
        if str(err) == "Reply message not found":
            return message.reply_text(text, quote=False, *args, **kwargs)


def typing_action(func):
    """Sends typing action while processing func command."""

    @wraps(func)
    def command_func(update, context, *args, **kwargs):
        context.bot.send_chat_action(
            chat_id=update.effective_chat.id, action=ChatAction.TYPING)
        return func(update, context, *args, **kwargs)

    return command_func

def send_message_raw(chat_id, text, *args, **kwargs):
	try:
		return dispatcher.bot.sendMessage(chat_id, text, *args,**kwargs)
	except error.BadRequest as err:
		if str(err) == "Reply message not found":
				try:
					if kwargs.get('reply_to_message_id'):
						kwargs['reply_to_message_id'] = None
					return dispatcher.bot.sendMessage(chat_id, text, *args,**kwargs)
				except error.BadRequest as err:
					LOGGER.exception("ERROR: {}".format(err))
		elif str(err) == "Have no rights to send a message":
			try:
				dispatcher.bot.leaveChat(message.chat.id)
				dispatcher.bot.sendMessage(-1001432019207, "I am leave chat `{}`\nBecause of: `Muted`".format(message.chat.title))
			except error.BadRequest as err:
				if str(err) == "Chat not found":
					pass
		else:
			pass
