"""
MIT License

Copyright (C) 2021 Awesome-RJ

This file is part of @Cutiepii_Robot (Telegram Bot)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import asyncio
import datetime

from telethon.tl import functions, types
from Cutiepii_Robot.events import register
from Cutiepii_Robot import ubot, telethn


async def is_register_admin(chat, user):
    if isinstance(chat, (types.InputPeerChannel, types.InputChannel)):
        return isinstance(
            (
                await telethn(functions.channels.GetParticipantRequest(chat, user))
            ).participant,
            (types.ChannelParticipantAdmin, types.ChannelParticipantCreator),
        )
    if isinstance(chat, types.InputPeerUser):
        return True


@register(pattern="^/gen (.*)")
async def alive(event):
    if event.is_group and not await is_register_admin(
        event.input_chat, event.message.sender_id
    ):
        return
    sender = await event.get_sender()
    fname = sender.first_name
    m = await event.reply("Generating CC...Pls Weit.")
    ok = event.pattern_match.group(1)
    async with ubot.conversation("@ccgen_robot") as bot_conv:
        await bot_conv.send_message("/generate")
        await bot_conv.send_message("💳Credit Card Generator💳")
        await asyncio.sleep(2)
        await bot_conv.send_message(ok)
        await asyncio.sleep(1)
        response = await bot_conv.get_response()
        await asyncio.sleep(1)
        await response.click(text="✅Generate✅")
        await asyncio.sleep(2)
        text = "****Generated Cards:****\n"
        gen = await bot_conv.get_response()
        card = gen.text
        text = f"{card.splitlines()[0]}\n"
        text += f"{card.splitlines()[1]}\n"
        text += f"{card.splitlines()[2]}\n"
        text += f"{card.splitlines()[3]}\n"
        text += f"{card.splitlines()[4]}\n"
        text += f"{card.splitlines()[5]}\n"
        text += f"\nGenerated By: **{fname}**"
        await m.edit(text)


@register(pattern="^/key (.*)")
async def alive(event):
    if event.is_group and not await is_register_admin(
        event.input_chat, event.message.sender_id
    ):
        return
    sender = await event.get_sender()
    fname = sender.first_name
    ok = event.pattern_match.group(1)
    k = await event.reply("**Wait for Result.**")
    start_time = datetime.datetime.now()
    async with ubot.conversation("@Carol5_bot") as bot_conv:
        await bot_conv.send_message(f"/key {ok}")
        await asyncio.sleep(6)
        response = await bot_conv.get_response()
        await event.delete()
        end_time = datetime.datetime.now()
        pingtime = end_time - start_time
        time = str(round(pingtime.total_seconds(), 2)) + "s"
        if "Invalid" in response.text:
            reply = f"SK Key : {ok}\n"
            reply += "Result: Invalid API Key\n"
            reply += "RESPONSE: ❌Invalid Key❌\n"
            reply += f"Time: {time}\n"
            reply += f"Checked By **{fname}**"
        elif "Test" in response.text:
            reply = "SK Key : sk_live_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n"
            reply += "Result: Test mode Key\n"
            reply += "RESPONSE: ❌Test Mode Key❌\n"
            reply += f"Time: {time}\n"
            reply += f"Checked By **{fname}**"
        elif "Valid" in response.text:
            reply = "SK Key : sk_live_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n"
            reply += "Result: LIVE\n"
            reply += "RESPONSE: ✅Valid Key\n"
            reply += f"Time: {time}\n"
            reply += f"Checked By **{fname}**"
        else:
            reply = "Error, Report @LunaBotSupport"
        await k.edit(reply)


@register(pattern="^/ss (.*)")
async def alive(event):
    if event.is_group and not await is_register_admin(
        event.input_chat, event.message.sender_id
    ):
        return
    sender = await event.get_sender()
    fname = sender.first_name
    ok = event.pattern_match.group(1)
    k = await event.reply("**Wait for Result.**")
    async with ubot.conversation("@Carol5_bot") as bot_conv:
        await bot_conv.send_message(f"/ss {ok}")
        await asyncio.sleep(9)
        response = await bot_conv.get_response()
        if "Try again after" in response.text:
            await k.edit(response)
            return
        if "Your date is invalid" in response.text:
            await k.edit("Format Wrong or invalid cc.")
            return
        res = response.text
        text = f"{res.splitlines()[0]}\n"
        text += f"{res.splitlines()[1]}\n"
        text += f"{res.splitlines()[2]}\n"
        text += f"{res.splitlines()[3]}\n"
        text += f"{res.splitlines()[4]}\n"
        text += f"{res.splitlines()[5]}\n"
        text += f"{res.splitlines()[6]}\n"
        text += f"Checked By **{fname}**"
        await k.edit(text)


@register(pattern="^/pp (.*)")
async def alive(event):
    if event.is_group and not await is_register_admin(
        event.input_chat, event.message.sender_id
    ):
        return
    sender = await event.get_sender()
    fname = sender.first_name
    ok = event.pattern_match.group(1)
    k = await event.reply("**Wait for Result.**")
    async with ubot.conversation("@Carol5_bot") as bot_conv:
        await bot_conv.send_message(f"/pp {ok}")
        await asyncio.sleep(14)
        response = await bot_conv.get_response()
        if "Try again after" in response.text:
            await k.edit(response)
            return
        if "Your date is invalid" in response.text:
            await k.edit("Format Wrong or invalid cc.")
            return
        res = response.text
        text = f"{res.splitlines()[0]}\n"
        text += f"{res.splitlines()[1]}\n"
        text += f"{res.splitlines()[2]}\n"
        text += f"{res.splitlines()[3]}\n"
        text += f"{res.splitlines()[4]}\n"
        text += f"{res.splitlines()[5]}\n"
        text += f"{res.splitlines()[6]}\n"
        text += f"Checked By **{fname}**"
        await k.edit(text)


@register(pattern="^/ch (.*)")
async def alive(event):
    if event.is_group and not await is_register_admin(
        event.input_chat, event.message.sender_id
    ):
        return
    sender = await event.get_sender()
    fname = sender.first_name
    ok = event.pattern_match.group(1)
    async with ubot.conversation("@Carol5_bot") as bot_conv:
        await bot_conv.send_message(f"/ch {ok}")
        k = await event.reply("**Wait for Result.**")
        await asyncio.sleep(18)
        response = await bot_conv.get_response()
        if "Try again after" in response.text:
            await k.edit(response)
            return
        if "Your date is invalid" in response.text:
            await k.edit("Format Wrong or invalid cc.")
            return
        res = response.text
        text = f"{res.splitlines()[0]}\n"
        text += f"{res.splitlines()[1]}\n"
        text += f"{res.splitlines()[2]}\n"
        text += f"{res.splitlines()[3]}\n"
        text += f"{res.splitlines()[4]}\n"
        text += f"{res.splitlines()[5]}\n"
        text += f"{res.splitlines()[6]}\n"
        text += f"Checked By **{fname}**"
        await k.edit(text)


@register(pattern="^/au (.*)")
async def alive(event):
    if event.is_group and not await is_register_admin(
        event.input_chat, event.message.sender_id
    ):
        return
    sender = await event.get_sender()
    fname = sender.first_name
    ok = event.pattern_match.group(1)
    async with ubot.conversation("@Carol5_bot") as bot_conv:
        await bot_conv.send_message(f"/au {ok}")
        k = await event.reply("**Wait for Result.**")
        await asyncio.sleep(18)
        response = await bot_conv.get_response()
        if "Try again after" in response.text:
            await event.reply(response)
            return
        if "Your date is invalid" in response.text:
            await event.reply("Format Wrong or invalid cc.")
            return
        res = response.text
        text = f"{res.splitlines()[0]}\n"
        text += f"{res.splitlines()[1]}\n"
        text += f"{res.splitlines()[2]}\n"
        text += f"{res.splitlines()[3]}\n"
        text += f"{res.splitlines()[4]}\n"
        text += f"{res.splitlines()[5]}\n"
        text += f"{res.splitlines()[6]}\n"
        text += f"Checked By **{fname}**"
        await k.edit(text)


@register(pattern="^/bin (.*)")
async def alive(event):
    if event.is_group and not await is_register_admin(
        event.input_chat, event.message.sender_id
    ):
        return
    sender = await event.get_sender()
    fname = sender.first_name
    k = await event.reply("**Wait for Result.**")
    ok = event.pattern_match.group(1)
    async with ubot.conversation("@Carol5_bot") as bot_conv:
        await bot_conv.send_message(f"/bin {ok}")
        await asyncio.sleep(5)
        response = await bot_conv.get_response()
        res = response.text
        if "❌" in res:
            text = "🤬❌ INVALID BIN ❌🤬\n"
        else:
            text = f"{res.splitlines()[0]}\n"
            text += f"{res.splitlines()[1]}\n"
            text += f"{res.splitlines()[2]}\n"
            text += f"{res.splitlines()[3]}\n"
            text += f"{res.splitlines()[4]}\n"
            text += f"{res.splitlines()[5]}\n"
            text += f"{res.splitlines()[6]}\n"

        text += f"Checked By **{fname}**"
        await k.edit(text)
