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

async def get_user_from_event(event):
    """Get the user from argument or replied message."""
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        user_obj = await bot.get_entity(previous_message.sender_id)
    else:
        user = event.pattern_match.group(1)

        if user.isnumeric():
            user = int(user)

        if not user:
            await event.reply(
                "**I don't know who you're talking about, you're going to need to specify a user...!**"
            )
            return

        if event.message.entities is not None:
            probable_user_mention_entity = event.message.entities[0]

            if isinstance(probable_user_mention_entity, MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                user_obj = await bot.get_entity(user_id)
                return user_obj
        try:
            user_obj = await bot.get_entity(user)
        except (TypeError, ValueError) as err:
            await event.reply(str(err))
            return None

    return user_obj


def find_instance(items, class_or_tuple):
    for item in items:
        if isinstance(item, class_or_tuple):
            return item
    return None
"""
@bot.on(events.NewMessage(pattern="/promote ?(.*)"))
async def promote(promt):
    if promt.is_group:
        if promt.sender_id == OWNER_ID:
            pass
        else:
          if not await can_promote_users(message=promt):
            return
    else:
        return
    user = await get_user_from_event(promt)
    if promt.is_group:
        if await is_register_admin(promt.input_chat, user.id):
            await promt.reply("**Well! i cant promote user who is already an admin**")
            return
        pass
    else:
        return
    new_rights = ChatAdminRights(
        add_admins=True,
        invite_users=True,
        change_info=True,
        ban_users=True,
        delete_messages=True,
        pin_messages=True,
    )
    if user:
        pass
    else:
        return
    quew = promt.pattern_match.group(1)
    if quew:
        title = quew
    else:
        title = "Admin"
    # Try to promote if current user is admin or creator
    try:
        await bot(EditAdminRequest(promt.chat_id, user.id, new_rights, title))
        await promt.reply("**Successfully promoted!**")
    # If Telethon spit BadRequestError, assume
    # we don't have Promote permission
    except Exception:
        await promt.reply("Failed to promote.")
        return
@bot.on(events.NewMessage(pattern="/demote(?: |$)(.*)"))
async def demote(dmod):
    if dmod.is_group:
        if not await can_promote_users(message=dmod):
            return
    else:
        return
    user = await get_user_from_event(dmod)
    if dmod.is_group:
        if not await is_register_admin(dmod.input_chat, user.id):
            await dmod.reply("**Hehe, i cant demote non-admin**")
            return
        pass
    else:
        return
    if user:
        pass
    else:
        return
    # New rights after demotion
    newrights = ChatAdminRights(
        add_admins=False,
        invite_users=False,
        change_info=False,
        ban_users=False,
        delete_messages=False,
        pin_messages=False,
    )
    # Edit Admin Permission
    try:
        await bot(EditAdminRequest(dmod.chat_id, user.id, newrights, "Admin"))
        await dmod.reply("**Demoted Successfully!**")
    # If we catch BadRequestError from Telethon
    # Assume we don't have permission to demote
    except Exception:
        await dmod.reply("**Failed to demote.**")
        return
"""

@bot.on(events.NewMessage(pattern="/lowpromote ?(.*)"))
async def lowpromote(promt):
    if promt.is_group:
        if promt.sender_id == OWNER_ID:
            pass
        else:
            if not await can_promote_users(message=promt):
                return
    else:
        return

    user = await get_user_from_event(promt)
    if promt.is_group:
        if await is_register_admin(promt.input_chat, user.id):
            await promt.reply("**Well! i cant promote user who is already an admin**")
            return
    else:
        return

    new_rights = ChatAdminRights(
        add_admins=False,
        invite_users=True,
        change_info=False,
        ban_users=False,
        delete_messages=True,
        pin_messages=False,
    )

    if user:
        pass
    else:
        return
    quew = promt.pattern_match.group(1)
    if quew:
        title = quew
    else:
        title = "Moderator"
    # Try to promote if current user is admin or creator
    try:
        await bot(EditAdminRequest(promt.chat_id, user.id, new_rights, title))
        await promt.reply("**Successfully promoted!**")

    # If Telethon spit BadRequestError, assume
    # we don't have Promote permission
    except Exception:
        await promt.reply("Failed to promote.")
        return 
