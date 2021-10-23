import asyncio
import time

from SaitamaRobot import SUDO_USERS, telethn
from telethon import events
from telethon.errors.rpcerrorlist import MessageDeleteForbiddenError
from telethon.tl.types import ChannelParticipantsAdmins


# Check if user has admin rights
async def is_administrator(user_id: int, message):
    admin = False
    async for user in client.iter_participants(
        message.chat_id, filter=ChannelParticipantsAdmins
    ):
        if user_id == user.id or user_id in SUDO_USERS:
            admin = True
            break
    return admin


@telethn.on(events.NewMessage(pattern="^[!/]purge$"))
async def purge_msg(event):
    chat = event.chat_id
    start = time.perf_counter()
    msgs = []

    if not await is_administrator(
        user_id=event.sender_id, message=event
    ) and event.from_id not in [1087968824]:
        await event.reply("You're Not An Admin!")
        return

    msg = await event.get_reply_message()
    if not msg:
        await event.reply("Reply to a message to select where to start purging from.")
        return

    try:
        msg_id = msg.id
        count = 0
        to_delete = event.message.id - 1
        await event.client.delete_messages(chat, event.message.id)
        msgs.append(event.reply_to_msg_id)
        for m_id in range(to_delete, msg_id - 1, -1):
            msgs.append(m_id)
            count += 1
            if len(msgs) == 100:
                await event.client.delete_messages(chat, msgs)
                msgs = []

        await event.client.delete_messages(chat, msgs)
        time_ = time.perf_counter() - start
        del_res = await event.client.send_message(
            event.chat_id, f"Purged {count} Messages In {time_:0.2f} Secs."
        )

        await asyncio.sleep(4)
        await del_res.delete()

    except MessageDeleteForbiddenError:
        text = "Failed to delete messages.\n"
        text += "Messages maybe too old or I'm not admin! or dont have delete rights!"
        del_res = await event.respond(text, parse_mode="md")
        await asyncio.sleep(5)
        await del_res.delete()


@telethn.on(events.NewMessage(pattern="^[!/]spurge$"))
async def spurge(event):
    chat = event.chat_id
    start = time.perf_counter()
    msgs = []

    if not await is_administrator(
        user_id=event.sender_id, message=event
    ) and event.from_id not in [1087968824]:
        await event.reply("You're Not An Admin!")
        return

    msg = await event.get_reply_message()
    if not msg:
        await event.reply("Reply to a message to select where to start purging from.")
        return

    try:
        msg_id = msg.id
        count = 0
        to_delete = event.message.id - 1
        await event.client.delete_messages(chat, event.message.id)
        msgs.append(event.reply_to_msg_id)
        for m_id in range(to_delete, msg_id - 1, -1):
            msgs.append(m_id)
            count += 1
            if len(msgs) == 100:
                await event.client.delete_messages(chat, msgs)
                msgs = []

        await event.client.delete_messages(chat, msgs)
        time.perf_counter() - start
        del_res = await event.client.send_message()

        await asyncio.sleep(4)
        await del_res.delete()

    except MessageDeleteForbiddenError:
        text = "Failed to delete messages.\n"
        text += "Messages maybe too old or I'm not admin! or dont have delete rights!"
        del_res = await event.respond(text, parse_mode="md")
        await asyncio.sleep(5)
        await del_res.delete()


@telethn.on(events.NewMessage(pattern="^[!/]del$"))
async def delete_msg(event):

    if not await is_administrator(
        user_id=event.sender_id, message=event
    ) and event.from_id not in [1087968824]:
        await event.reply("You're not an admin!")
        return

    chat = event.chat_id
    msg = await event.get_reply_message()
    if not msg:
        await event.reply("Reply to some message to delete it.")
        return
    to_delete = event.message
    chat = await event.get_input_chat()
    rm = [msg, to_delete]
    await event.client.delete_messages(chat, rm)


@telethn.on(events.NewMessage(pattern="^[!/]spam$"))
async def report_spam(event):
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


__mod_name__ = "Purges"

__help__ = """
**Admin commands:**
- /purge: Delete all messages from the replied to message, to the current message.
- /purge <X>: Delete the following X messages after the replied to message.
- /spurge: Same as purge, but doesnt send the final confirmation message.
- /del: Deletes the replied to message.
- /purgefrom: Reply to a message to mark the message as where to purge from - this should be used followed by a /purgeto.
- /purgeto: Delete all messages between the replied to message, and the message marked by the latest /purgefrom. Mark the message to purge to (as a reply). All messages between the previously marked /purgefrom and the newly marked /purgeto will be deleted.
**Example**

-> `/purgefrom`
- Mark the message to purge to (as a reply). All messages between the previously marked /purgefrom and the newly marked /purgeto will be deleted.
-> `/purgeto`
"""
