from telethon import functions, types
from SaitamaRobot.client import new_message
from SaitamaRobot import telethn, SUDO_USERS, ASSE_USERS, DEV_USERS, TEMPORARY_DATA, OWNER_ID, SUPPORT_USERS, WHITELIST_USERS
from telethon import events, Button
from asyncio import sleep
from os import remove
import os
import json
import asyncio
import wget
import math
import time
from tswift import Song
from telethon.tl.types import DocumentAttributeAudio

from youtubesearchpython import SearchVideos
from SaitamaRobot.events import register
from SaitamaRobot.modules.helper_funcs.telethn.chatstatus import (
    can_delete_messages, user_is_admin, haruka_is_admin, can_ban_users)
    
from telethon.errors import (BadRequestError, ChatAdminRequiredError,
                             ImageProcessFailedError, PhotoCropSizeSmallError,
                             UserAdminInvalidError)
from telethon.errors.rpcerrorlist import (UserIdInvalidError,
                                          MessageTooLongError)
from telethon.tl.functions.channels import (EditAdminRequest,
                                            EditBannedRequest,
                                            EditPhotoRequest)
from telethon.tl.types import (ChannelParticipantsAdmins, ChatAdminRights,
                               ChatBannedRights, MessageEntityMentionName,
                               MessageMediaPhoto, ChannelParticipantCreator)
from telethon.tl.types import UserStatusLastMonth, UserStatusLastWeek
from SaitamaRobot.events import register, edit_or_reply
from SaitamaRobot.modules.languages import tl
import SaitamaRobot.modules.sql.feds_sql as sql

from youtube_dl import YoutubeDL
from youtube_dl.utils import (
    ContentTooShortError,
    DownloadError,
    ExtractorError,
    GeoRestrictedError,
    MaxDownloadsReached,
    PostProcessingError,
    UnavailableVideoError,
    XAttrMetadataError,
)


# =================== CONSTANT ===================

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

MUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=True)

UNMUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=False)
# ================================================

async def is_administrator(user_id: int, message):
    admin = False
    async for user in message.client.iter_participants(
        message.chat_id, filter=ChannelParticipantsAdmins
    ):
        if user_id == user.id or user_id in DEV_USERS or user_id in ASSE_USERS:
            admin = True
            break
    return admin

async def can_promote_users(message):
    result = await telethn(
        functions.channels.GetParticipantRequest(
            channel=message.chat_id,
            user_id=message.sender_id,
        )
    )
    p = result.participant
    return isinstance(p, types.ChannelParticipantCreator) or (
        isinstance(p, types.ChannelParticipantAdmin) and p.admin_rights.ban_users
    )

async def c(event):
   msg = 0
   async for x in event.client.iter_participants(event.chat_id, filter=ChannelParticipantsAdmins):
    if isinstance(x.participant, ChannelParticipantCreator):
       msg += x.id
   return msg

async def can_ban_users(message):
    result = await telethn(
        functions.channels.GetParticipantRequest(
            channel=message.chat_id,
            user_id=message.sender_id,
        ))
    p = result.participant
    return isinstance(p, types.ChannelParticipantCreator) or (isinstance(
        p, types.ChannelParticipantAdmin) and p.admin_rights.ban_users)


async def get_user_from_event(event):
    """ Get the user from argument or replied message. """
    args = event.pattern_match.group(1).split(' ', 1)
    extra = None
    if event.reply_to_msg_id and not len(args) == 2:
        previous_message = await event.get_reply_message()
        user_obj = await event.client.get_entity(previous_message.from_id)
        extra = event.pattern_match.group(1)
    elif args:
        user = args[0]
        if len(args) == 2:
            extra = args[1]

        if user.isnumeric():
            user = int(user)

        if not user:
            return await event.reply("`Pass the user's username, id or reply!`")

        if event.message.entities is not None:
            probable_user_mention_entity = event.message.entities[0]

            if isinstance(probable_user_mention_entity,
                          MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                user_obj = await event.client.get_entity(user_id)
                return user_obj
        try:
            user_obj = await event.client.get_entity(user)
        except (TypeError, ValueError) as err:
            return await event.reply(str(err))

    return user_obj, extra

async def get_user_from_id(user, event):
    if isinstance(user, str):
        user = int(user)

    try:
        user_obj = await event.client.get_entity(user)
    except (TypeError, ValueError) as err:
        return await event.reply(str(err))

    return user_obj

async def _is_user_fed_admin(fed_id, user_id):
    fed_admins = sql.all_fed_users(fed_id)
    if fed_admins is False:
        return False
    if int(user_id) in fed_admins or int(user_id) == OWNER_ID:
        return True
    else:
        return False
# ============================ Modules ================================================
@register(pattern="^/iban(?: |)(.*)")
async def ban(bon):
    """ For .ban command, bans the replied/tagged person """
    # Here laying the sanity check
    chat = await bon.get_chat()

    if bon.from_id == None:
      return

    if not bon.is_group:
        await bon.reply("**I don't think this is a group**")
        return
    if bon.is_group:
        if not await can_ban_users(message=bon):
            await bon.reply("You Don't have permission to ban a user")
            return

    chat = await bon.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    if not await user_is_admin(user_id=bon.sender_id, message=bon):
      await bon.reply("You need to be a admin to ban him")
      return


    # Well
    user, reason = await get_user_from_event(bon)
    if user:
        pass
    else:
        return

    if user.id == (await bon.client.get_me()).id:
        await bon.reply("`Why would i ban myself.. KEK`")
        return

    if user.id == OWNER_ID:
        await bon.reply("I'm not gonna ban my master")
        return

    if int(user.id) in SUDO_USERS + SUPPORT_USERS:
        await bon.reply("I'm not gonna ban bots Sudo or devs")
        return
    
    if int(user.id) in DEV_USERS + ASSE_USERS:
        await bon.reply("I'm not gonna ban bot devs")
        return
    
    if int(user.id) in WHITELIST_USERS:
        await bon.reply("This User Mark As Whitelisted")
        return

    # Announce that we're going to whack the pest
    try:
        await bon.client(EditBannedRequest(bon.chat_id, user.id,
                                           BANNED_RIGHTS))
    except BadRequestError:
        await bon.reply('**insufficient rights:** may be i am not admin or you are try to ban an admin')
        return
    # Helps ban group join spammers more easily
    try:
        reply = await bon.get_reply_message()
        if reply:
            await reply.delete()
    except BadRequestError:
        await bon.reply(
            "`I dont have message nuking rights! But still he was banned!`")
        return
    # Delete message and then tell that the command
    # is done gracefully
    # Shout out the ID, so that fedadmins can fban later
    if reason:
        await bon.reply(f"User [{user.first_name}](tg://user?id={user.id}) was banned !!\
        \nID: `{str(user.id)}`\
        \nReason: {reason}")
    else:
        await bon.reply(f"User [{user.first_name}](tg://user?id={user.id}) was banned !!\
        \nID: `{str(user.id)}`")

@register(pattern="^/iunban(?: |)(.*)")
async def nothanos(unbon):
    """ For .unban command, unbans the replied/tagged person """
    # Here laying the sanity check
    chat = await unbon.get_chat()

    if unbon.from_id == None:
      return

    if not unbon.is_group:
        await unbon.reply("**I don't think this is group**")
        return
    if unbon.is_group:
        if not await can_ban_users(message=unbon):
            await unbon.reply("**You Don't have permission to unban a user**")
            return

    chat = await unbon.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    if not await user_is_admin(user_id=unbon.sender_id, message=unbon):
      await unbon.reply("You need to be an admin to unban him")
      return

    # Well
    # If everything goes well...
    user = await get_user_from_event(unbon)
    user = user[0]
    if user:
        pass
    else:
        return

    try:
        await unbon.client(
            EditBannedRequest(unbon.chat_id, user.id, UNBAN_RIGHTS))
        await unbon.reply("```Unbanned Successfully```")

    except UserIdInvalidError:
        await unbon.reply("`Uh oh my unban logic dead!`")

@telethn.on(events.NewMessage(pattern="^[/!]cleaninactive$"))
async def _(event):
    if event.fwd_from:
        return

    if event.is_group:
        if not await can_ban_users(message=event):
            await event.reply("You Are Missing Rights CanBanUsers")
    else:
        return

    c = 0
    KICK_RIGHTS = ChatBannedRights(until_date=None, view_messages=True)
    done = await event.reply("Kicking ...")
    async for i in telethn.iter_participants(event.chat_id):

        if isinstance(i.status, UserStatusLastMonth):
            status = await telethn(
                EditBannedRequest(event.chat_id, i, KICK_RIGHTS))
            if not status:
                return
            c = c + 1

        if isinstance(i.status, UserStatusLastWeek):
            status = await telethn(
                EditBannedRequest(event.chat_id, i, KICK_RIGHTS))
            if not status:
                return
            c = c + 1

    if c == 0:
        await done.reply("Everyone is Active Here Congo")
        return

    required_string = "Successfully Kicked **{}** users"
    await event.reply(required_string.format(c))



@telethn.on(events.CallbackQuery(data=b'rmdel'))
async def _(event):
    x = await event.client.get_entity(event.chat_id)
    title = x.title
    all_deleted = False
    if not await is_administrator(user_id=event.query.user_id, message=event):
        return
    async for user in event.client.iter_participants(event.chat_id):
        if user.deleted:
            try:
                await event.client(
                    EditBannedRequest(event.chat_id, user.id, BANNED_RIGHTS))
                all_deleted = True
            except Exception as e: 
                print(e)
                
    if all_deleted is True:
          await event.client.edit_message(event.chat_id,event.query.msg_id,f"Removed all deleted accounts in **{title}**.")
                
@new_message(pattern="^/cleandeleted$")
async def rm_deletedacc(show):
    if not show.is_group:
        await event.reply("`I don't think this is a group.`")
        return
    chat = await show.get_chat()
    admin = chat.admin_rights
    if not admin:
        await show.reply("I'm not admin!")
        return
    if not await user_is_admin(user_id=show.sender_id, message=show):
        await show.reply("Who dis non-admin telling me what to do? You want a kick?")
        return
    if not await can_ban_users(message=show):
        await show.reply("Seems like You don't have permission to ban users.")
        return
    del_u = 0
    del_status = "No deleted accounts found, Group is clean."
    x = await show.reply("Searching for deleted accounts...")
    async for user in show.client.iter_participants(show.chat_id):
        if user.deleted:
            del_u += 1
            await sleep(1)
    if del_u > 0:
        await show.client.delete_messages(show.chat_id, x.id)
        del_status = f"Found **{del_u}** deleted/zombies account(s) in this group,\
            \nclean them by clicking the button below."
        await show.client.send_message(show.chat_id, del_status, buttons=[Button.inline('Clean Zombies', b'rmdel')], reply_to=show.id)
    else:
        await show.client.edit_message(show.chat_id, x.id, del_status)

@telethn.on(events.CallbackQuery)
async def _(event):
   rights = await is_administrator(event.query.user_id, event)
   creator = await c(event)
   if event.data == b'rmapp':
       if not rights:
             await event.answer("You need to be admin to do this.")
             return
       if creator != event.query.user_id and event.query.user_id not in SUDO_USERS:
             await event.answer("Only owner of the chat can do this.")
             return
             #r = await event.get_reply_message()
       await event.client.unpin_message(event.chat_id)
       
       await event.client.edit_message(event.chat_id, event.query.msg_id, f"all pinned messages unpinned  in chat.")

   if event.data == b'can':
        if not rights:
             await event.answer("You need to be admin to do this in this chat.")
             return
        if creator != event.query.user_id and event.query.user_id not in SUDO_USERS:
             await event.answer("Only owner of the chat can cancel this operation.")
             return
        await event.client.edit_message(event.chat_id, event.query.msg_id, f"Removing of all unpinned has been cancelled.")

@new_message(pattern="^/unpinall$")
async def _(event):
  chat = await event.get_chat()
  creator = await c(event)
  if creator != event.sender_id and event.sender_id not in SUDO_USERS:
      await event.reply("Only the chat owner can unpin All at once.")
      return
  msg = f"Are you sure you would like to unpin ALL Pinned in {event.chat.title}? This action cannot be undone."
  await event.client.send_message(event.chat_id, msg, buttons=[[Button.inline('Unpin All', b'rmapp')], [Button.inline('Cancel', b'can')]], reply_to=event.id)

@telethn.on(events.NewMessage(pattern="^[!/]tagall$"))
async def tagging_powerful(event):
    mentions = "Checkout"
    chat = await event.get_input_chat()
    async for x in telethn.iter_participants(chat, 100):
        mentions += f"[\u2063](tg://user?id={x.id})"
    await event.reply(mentions)
    await event.delete()

@register(pattern="/music(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    if not event.is_group:
        await event.reply("`This Option is No More Available For Private`")
        return
    creator = await c(event)
    if event.sender_id not in SUDO_USERS:
      await event.reply("This Module Only For Sudo You Have to Use `/Song <song name>`.")
      return
    urlissed = event.pattern_match.group(1)
    myself_stark = await edit_or_reply(
        event, f"`Getting {urlissed} From Youtube Servers. Please Wait.`"
    )
    search = SearchVideos(f"{urlissed}", offset=1, mode="dict", max_results=1)
    mi = search.result()
    mio = mi["search_result"]
    mo = mio[0]["link"]
    thum = mio[0]["title"]
    fridayz = mio[0]["id"]
    thums = mio[0]["channel"]
    kekme = f"https://img.youtube.com/vi/{fridayz}/hqdefault.jpg"
    await asyncio.sleep(0.6)
    if not os.path.isdir("./music/"):
        os.makedirs("./music/")
    path = TEMPORARY_DATA
    sedlyf = wget.download(kekme, out=path)
    stark = (
        f'youtube-dl --force-ipv4 -q -o "./music/%(title)s.%(ext)s" --extract-audio --audio-format mp3 --audio-quality 128k '
        + mo
    )
    os.system(stark)
    await asyncio.sleep(4)
    km = f"./music/{thum}.mp3"
    if os.path.exists(km):
        await myself_stark.edit("`Song Downloaded Sucessfully. Let Me Upload it Here.`")
    else:
        await myself_stark.edit("`SomeThing Went Wrong. Try Again After Sometime..`")
    capy = f"**Song Name ➠** `{thum}` \n**Requested For ➠** `{urlissed}` \n**Channel ➠** `{thums}` \n**Link ➠** `{mo}`"
    await telethn.send_file(
        event.chat_id,
        km,
        force_document=False,
        allow_cache=False,
        caption=capy,
        thumb=sedlyf,
        performer=thums,
        supports_streaming=True,
    )
    await myself_stark.edit("`Song Uploaded.`")
    for files in (sedlyf, km):
        if files and os.path.exists(files):
            os.remove(files)

#JULIASONG = "@Anierobot_bot"
#JULIAVSONG = "@Anierobot_bot"

@register(pattern="^!song (.*)")
async def download_song(v_url):
    if not v_url.is_group:
        await v_url.reply(f"`This Option is No More Available For Private Add Our Bot Into Your Group For Use This Feature`",buttons=[Button.url(text='Add Bot', url="http://telegram.me/Anierobot_bot?startgroup=botstart")])
        #await v_url.client.send_message(v_url.chat_id, buttons=[Button.url(text='Add Bot', url="")])
        return        
    url = v_url.pattern_match.group(1)
    rkp = await v_url.reply("`Processing ...`")
    if not url:
        await rkp.reply("`Error \nusage song <song name>`")
    search = SearchVideos(url, offset=1, mode="json", max_results=1)
    test = search.result()
    p = json.loads(test)
    q = p.get('search_result')
    try:
        url = q[0]['link']
    except BaseException:
        return await rkp.reply("`Failed to find that song`")
    type = "audio"
    await rkp.edit("`Preparing to download ...`")
    if type == "audio":
        opts = {
            'format':
            'bestaudio',
            'addmetadata':
            True,
            'key':
            'FFmpegMetadata',
            'writethumbnail':
            True,
            'prefer_ffmpeg':
            True,
            'geo_bypass':
            True,
            'nocheckcertificate':
            True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
            }],
            'outtmpl':
            '%(id)s.mp3',
            'quiet':
            True,
            'logtostderr':
            False
        }
        video = False
        song = True
    try:
        await rkp.edit("`Fetching data, please wait ...`")
        with YoutubeDL(opts) as rip:
            rip_data = rip.extract_info(url)
    except DownloadError as DE:
        await rkp.reply(f"`{str(DE)}`")
        return
    except ContentTooShortError:
        await rkp.reply("`The download content was too short.`")
        return
    except GeoRestrictedError:
        await rkp.reply(
            "`Video is not available from your geographic location due to geographic restrictions imposed by a website.`"
        )
        return
    except MaxDownloadsReached:
        await rkp.reply("`Max-downloads limit has been reached.`")
        return
    except PostProcessingError:
        await rkp.reply("`There was an error during post processing.`")
        return
    except UnavailableVideoError:
        await rkp.reply("`Media is not available in the requested format.`")
        return
    except XAttrMetadataError as XAME:
        await rkp.reply(f"`{XAME.code}: {XAME.msg}\n{XAME.reason}`")
        return
    except ExtractorError:
        await rkp.reply("`There was an error during info extraction.`")
        return
    except Exception as e:
        await rkp.reply(f"{str(type(e)): {str(e)}}")
        return
    c_time = time.time()
    if song:
        await rkp.edit(f"`Sending the song ...`")
        #await asyncio.sleep(60)
        #user, reason = await get_user_from_event(v_url)

        y = await v_url.client.send_file(
            v_url.chat_id,
            f"{rip_data['id']}.mp3",
            supports_streaming=False,
            force_document=False,
            allow_cache=False,
            attributes=[
                DocumentAttributeAudio(duration=int(rip_data['duration']),
                                       title=str(rip_data['title']),
                                       performer=str(rip_data['uploader']))
            ])
        await rkp.edit("`Sending Song Success:`")
        os.system("rm -rf *.mp3")
        os.system("rm -rf *.webp")

@telethn.on(events.NewMessage(pattern="^[!/]fedadmin$"))
async def fedadmin(event):
    if not event.is_group:
        await message.reply("This command is specific to the group, not to our pm!")
        return ""
    fed_id = sql.get_fed_id(event.chat_id)

    if not fed_id:
        await event.reply(
            "This group is not in any federation!")
        return

    if await _is_user_fed_admin(fed_id, event.sender_id) is False:
        await event.reply(
            "Only federation admins can do this!")
        return
    info = sql.get_fed_info(fed_id)
    text = "**Federation Admin {}:**\n\n".format(info['fname'])
    text += "👑 Owner:\n"
    owner = await event.client.get_entity(int(info['owner']))
    try:
        owner_name = owner.first_name + " " + owner.last_name
    except:
        owner_name = owner.first_name
    text += " • [{}]({})\n".format(owner_name, owner.id)

    members = sql.all_fed_members(fed_id)
    if len(members) == 0:
        text += "\n🔱 There are no admins in this federation"
    else:
        text += "\n🔱 Admin:\n"
        for x in members:
            try:
                user = await event.client.get_entity(x)
                text += " • [{}]({})\n".format(user.first_name, user.id)
            except:
                pass
    await event.reply(text)
