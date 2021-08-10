import os
from time import sleep
import asyncio
from telethon import *
from telethon import events
from telethon.errors import *
from telethon.errors import FloodWaitError
from telethon.tl import *
from telethon.tl import functions, types
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.functions.channels import EditAdminRequest, EditBannedRequest
from telethon.tl.types import *
from telethon.tl.types import (
    ChatAdminRights,
    ChatBannedRights,
    MessageEntityMentionName,
)
from telethon.errors.rpcerrorlist import UserNotParticipantError
from AlainX import OWNER_ID
from AlainX import bot

# =================== CONSTANT ===================
PP_TOO_SMOL = "**The image is too small**"
PP_ERROR = "**Failure while processing image**"
NO_ADMIN = "**I am not an admin**"
NO_PERM = "**I don't have sufficient permissions!**"

CHAT_PP_CHANGED = "**Chat Picture Changed**"
CHAT_PP_ERROR = (
    "**Some issue with updating the pic,**"
    "**maybe you aren't an admin,**"
    "**or don't have the desired rights.**"
)
INVALID_MEDIA = "Invalid Extension"
BANNED_RIGHTS = ChatBannedRights(
    until_date=None,
    view_messages=True,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True,
)
UNBAN_RIGHTS = ChatBannedRights(
    until_date=None,
    send_messages=None,
    send_media=None,
    send_stickers=None,
    send_gifs=None,
    send_games=None,
    send_inline=None,
    embed_links=None,
)
KICK_RIGHTS = ChatBannedRights(until_date=None, view_messages=True)
MUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=True)
UNMUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=False)


import functools

def is_admin(func):
functools.wraps(func)
    async def a_c(event):
        if event.is_private:
          return await event.reply("This command is made to be used in group chats, not in pm!")
        is_admin = False
        suk = event
        if event.from_id == None:
          text = "Click to prove anonymous rights"
          buttons = Button.inline("Click to prove Anonymous", data="six")
          await event.reply(text, buttons=buttons)
          @tbot.on(events.CallbackQuery(pattern=r"six"))
          async def lodu(event):
            await asyncio.sleep(0.1)
            _s = await event.client.get_permissions(event.chat_id, event.sender_id)
            try:
             await func(suk, _s)
            except Exception as e:
              print(e)
          return
        try:
                _s = await event.client.get_permissions(event.chat_id, event.sender_id)
                if _s.is_admin:
                    is_admin = True
        except:
                is_admin = False
        if is_admin:
            await func(event, _s)
        elif not is_admin:
            await event.reply("Only Admins can execute this command!")
    return a_c

async def is_register_admin(chat, user):
    if isinstance(chat, (types.InputPeerChannel, types.InputChannel)):
        return isinstance(
            (
                await bot(functions.channels.GetParticipantRequest(chat, user))
            ).participant,
            (types.ChannelParticipantAdmin, types.ChannelParticipantCreator),
        )
    if isinstance(chat, types.InputPeerUser):
        return True


async def can_promote_users(message):
    result = await bot(
        functions.channels.GetParticipantRequest(
            channel=message.chat_id,
            participant=message.sender_id,
        )
    )
    p = result.participant
    return isinstance(p, types.ChannelParticipantCreator) or (
        isinstance(p, types.ChannelParticipantAdmin) and p.admin_rights.ban_users
    )

async def can_ban_users(message):
    result = await bot(
        functions.channels.GetParticipantRequest(
            channel=message.chat_id,
            participant=message.sender_id,
        )
    )
    p = result.participant
    return isinstance(p, types.ChannelParticipantCreator) or (
        isinstance(p, types.ChannelParticipantAdmin) and p.admin_rights.ban_users
    )

async def can_change_info(message):
    result = await bot(
        functions.channels.GetParticipantRequest(
            channel=message.chat_id,
            participant=message.sender_id,
        )
    )
    p = result.participant
    return isinstance(p, types.ChannelParticipantCreator) or (
        isinstance(p, types.ChannelParticipantAdmin) and p.admin_rights.change_info
    )


async def can_del(message):
    result = await bot(
        functions.channels.GetParticipantRequest(
            channel=message.chat_id,
            participant=message.sender_id,
        )
    )
    p = result.participant
    return isinstance(p, types.ChannelParticipantCreator) or (
        isinstance(p, types.ChannelParticipantAdmin) and p.admin_rights.delete_messages
    )


async def can_pin_msg(message):
    result = await bot(
        functions.channels.GetParticipantRequest(
            channel=message.chat_id,
            participant=message.sender_id,
        )
    )
    p = result.participant
    return isinstance(p, types.ChannelParticipantCreator) or (
        isinstance(p, types.ChannelParticipantAdmin) and p.admin_rights.pin_messages
    )


async def get_user_sender_id(user, event):
    if isinstance(user, str):
        user = int(user)

    try:
        user_obj = await bot.get_entity(user)
    except (TypeError, ValueError) as err:
        await event.edit(str(err))
        return None

    return user_obj
