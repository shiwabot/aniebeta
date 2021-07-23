from telethon import events
from SaitamaRobot import SUDO_USERS, telethn


async def edit_or_reply(event, text):
    if event.sender_id in SUDO_USERS:
        reply_to = await event.get_reply_message()
        if reply_to:
            return await reply_to.reply(text)
        return await event.reply(text)
    return await event.reply(text)

def register(**args):
    """ Registers a new message. """
    pattern = args.get('pattern', None)

    r_pattern = r'^[/!]'

    if pattern is not None and not pattern.startswith('(?i)'):
        args['pattern'] = '(?i)' + pattern

    args['pattern'] = pattern.replace('^/', r_pattern, 1)

    def decorator(func):
        telethn.add_event_handler(func, events.NewMessage(**args))
        return func

    return decorator

def callbackquery(**args):
    """ Registers inline query. """
    def decorator(func):
        telethn.add_event_handler(func, events.CallbackQuery(**args))
        return func

    return decorator
