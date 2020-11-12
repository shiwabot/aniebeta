from SaitamaRobot.modules.helper_funcs.telethn.chatstatus import (
    can_delete_messages, user_is_admin)
from SaitamaRobot import telethn
import time
from telethon import events
from telethon.tl.types import ChannelParticipantsAdmins
from telethon.errors.rpcerrorlist import MessageDeleteForbiddenError
from SaitamaRobot import SUDO_USERS

from telethon.tl.functions.channels import GetParticipantRequest

async def user_can_delete_t(chat_id, user_id, message):
    
    result = await message.client(GetParticipantRequest(
        channel=chat_id,
        user_id=user_id
    ))
    status = result.participant.admin_rights.delete_messages
    if status or user_id in SUDO_USERS:
        return True
    else:
        return False

@telethn.on(events.NewMessage(pattern="^[!/]purge$"))
async def purge_messages(event):
    start = time.perf_counter()
    if event.from_id is None:
        return

    if not await user_is_admin(user_id=event.from_id, message=event):
        await event.reply("Only Admins are allowed to use this command")
        return
        result = await message.client(GetParticipantRequest(
        channel=chat_id,
        user_id=user_id
    ))

    if not await can_delete_messages(message=event):
        await event.reply("Can't seem to purge the message")
        return

    if not await user_can_delete_t(event.chat_id, event.from_id, event):
        await event.reply("You do not have enough rights to delete messages.")
        return
    
    reply_msg = await event.get_reply_message()
    if not reply_msg:
        await event.reply(
            "Reply to a message to select where to start purging from.")
        return
    messages = []
    message_id = reply_msg.id
    delete_to = event.message.id

    messages.append(event.reply_to_msg_id)
    for msg_id in range(message_id, delete_to + 1):
        messages.append(msg_id)
        if len(messages) == 100:
            await event.client.delete_messages(event.chat_id, messages)
            messages = []

    await event.client.delete_messages(event.chat_id, messages)
    time_ = time.perf_counter() - start
    text = f"Purged Successfully in {time_:0.2f} Second(s)"
    await event.respond(text, parse_mode='markdown')

@telethn.on(events.NewMessage(pattern="^[!/]del$"))
async def delete_messages(event):
    if event.from_id is None:
        return

    if not await user_is_admin(user_id=event.from_id, message=event):
        await event.reply("Only Admins are allowed to use this command")
        return
        result = await message.client(GetParticipantRequest(
        channel=chat_id,
        user_id=user_id
    ))

    if not await can_delete_messages(message=event):
        await event.reply("Can't seem to purge the message")
        return

    if not await user_can_delete_t(event.chat_id, event.from_id, event):
        await event.reply("You do not have enough rights to delete messages.")
        return

    message = await event.get_reply_message()
    if not message:
        await event.reply("Whadya want to delete?")
        return
    chat = await event.get_input_chat()
    del_message = [message, event.message]
    await event.client.delete_messages(chat, del_message)


__help__ = """
*Admin only:*
 - /del: deletes the message you replied to
 - /purge: deletes all messages between this and the replied to message.
 - /purge <integer X>: deletes the replied message, and X messages following it if replied to a message.
"""

__mod_name__ = "Purges"
