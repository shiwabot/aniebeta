from SaitamaRobot.modules.helper_funcs.telethn.chatstatus import (
    can_delete_messages, user_is_admin)
from SaitamaRobot import telethn
import time
from telethon import events
from telethon.tl.types import ChannelParticipantsAdmins
from telethon.errors.rpcerrorlist import MessageDeleteForbiddenError
from SaitamaRobot import SUDO_USERS
import asyncio

from telethon.tl.functions.channels import GetParticipantRequest

async def user_can_delete_t(chat_id, user_id, message):
    res = False
    result = await message.client(GetParticipantRequest(
        user_id=user_id,
        channel=chat_id
    ))
    try:
        status = result.participant.admin_rights.delete_messages
    except AttributeError:
        res = True
        return res
    if status:
        res = True
    return res

@telethn.on(events.NewMessage(pattern="^[!/]purge$"))
async def purge_messages(event):
    start = time.perf_counter()
    if event.sender_id is None:
        return

    if not await user_is_admin(user_id=event.sender_id, message=event):
        await event.reply("Only Admins are allowed to use this command")
        return
        result = await message.client(GetParticipantRequest(
        channel=chat_id,
        user_id=user_id
    ))

    if not await can_delete_messages(message=event):
        await event.reply("Can't seem to purge the message")
        return

    if not await user_can_delete_t(event.chat_id, event.sender_id, event):
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
    text = f"Purged Successfully in {time_:0.2f} Second(s) This Message Self Destruct After 4 Seconds"
    x = await event.respond(text, parse_mode='markdown')
    await asyncio.sleep(4)
    await event.client.delete_messages(event.chat_id, x.id)

@telethn.on(events.NewMessage(pattern="^[!/]del$"))
async def delete_messages(event):
    if event.sender_id is None:
        return

    if not await user_is_admin(user_id=event.sender_id, message=event):
        await event.reply("Only Admins are allowed to use this command")
        return

    if not await can_delete_messages(message=event):
        await event.reply("Can't seem to purge the message")
        return

    if not await user_can_delete_t(event.chat_id, event.sender_id, event):
        await event.reply("You do not have enough rights to delete messages.")
        return

    message = await event.get_reply_message()
    if not message:
        await event.reply("Want You Want to delete?")
        return
    chat = await event.get_input_chat()
    del_message = [message, event.message]
    await event.client.delete_messages(chat, del_message)

@telethn.on(events.NewMessage(pattern="^[!/]spam$"))
async def _(event):
    if event.fwd_from:
        return
    mentions = "@admin: **Spam Spotted**"
    chat = await event.get_input_chat()
    async for x in telethn.iter_participants(chat, filter=ChannelParticipantsAdmins):
        mentions += f"[\u2063](tg://user?id={x.id})"
    reply_message = None
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
        await reply_message.reply(mentions)
    else:
        await event.reply(mentions)
    await event.delete()


__help__ = """
*Admin only:*
 - /del: deletes the message you replied to
 - /purge: deletes all messages between this and the replied to message.
 - /purge <integer X>: deletes the replied message, and X messages following it if replied to a message.
"""

__mod_name__ = "Purges"
