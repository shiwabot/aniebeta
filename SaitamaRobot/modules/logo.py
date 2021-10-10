import os
import random

from PIL import Image, ImageDraw, ImageFont
from telethon.tl.types import InputMessagesFilterDocument as fdocu
from telethon.tl.types import InputMessagesFilterPhotos as fphot

from SaitamaRobot import OWNER_ID
from SaitamaRobot import telethn as tbot
from SaitamaRobot import ubot
from SaitamaRobot.events import register

# needed to dynamically load modules
# NOTE: Module order is not guaranteed, specify that in the config file!


@register(pattern="^/logo ?(.*)")
async def lego(event):
    quew = event.pattern_match.group(1)
    if event.sender_id == OWNER_ID:
        pass
    else:

        if not quew:
            await event.reply("```Provide Some Text To Draw!```")
            return
        else:
            pass
    await event.reply("```Creating logo...wait!```")
    try:
        bheysed = []

        async for aln in ubot.iter_messages("@AnieLogo", filter=fphot):

            bheysed.append(aln)
        jased = random.choice(bheysed)
        klrd = await jased.download_media()
        text = event.pattern_match.group(1)
        img = Image.open(klrd)
        draw = ImageDraw.Draw(img)
        image_widthz, image_heightz = img.size
        bheysed1 = []

        async for alan in ubot.iter_messages("@Aniefont", filter=fdocu):

            bheysed1.append(alan)
        nsed = random.choice(bheysed1)
        fekod = await nsed.download_media()
        font = ImageFont.truetype(fekod, 100)
        w, h = draw.textsize(text, font=font)
        h += int(h * 0.21)
        image_width, image_height = img.size
        draw.text(
            ((image_widthz - w) / 2, (image_heightz - h) / 2),
            text,
            font=font,
            fill=(200, 200, 200),
        )
        x = (image_widthz - w) / 2
        y = (image_heightz - h) / 2 + 6
        draw.text(
            (x, y), text, font=font, fill="white", stroke_width=3, stroke_fill="black"
        )
        fname2 = "LogoByAnie.png"
        img.save(fname2, "png")
        await tbot.send_file(
            event.chat_id,
            fname2,
            caption="Made By {} via [Anie](https://t.me/Aniebotsupports)",
        )
        if os.path.exists(fname2):
            os.remove(fname2)
    except Exception as e:
        await event.reply(f"Error Report @Aniebotsupports, {e}")


@register(pattern="^/wlogo ?(.*)")
async def lego(event):
    quew = event.pattern_match.group(1)
    if event.sender_id == OWNER_ID:
        pass
    else:

        if not quew:
            await event.reply("Provide Some Text To Draw!")
            return
        else:
            pass
    await event.reply("Creating your logo...wait!")
    try:
        text = event.pattern_match.group(1)
        img = Image.open("./SaitamaRobot/resources/blackbg.jpg")
        draw = ImageDraw.Draw(img)
        image_widthz, image_heightz = img.size
        font = ImageFont.truetype("./SaitamaRobot/resources/Maghrib.ttf", 1000)
        w, h = draw.textsize(text, font=font)
        h += int(h * 0.21)
        image_width, image_height = img.size
        draw.text(
            ((image_widthz - w) / 2, (image_heightz - h) / 2),
            text,
            font=font,
            fill=(255, 255, 255),
        )
        x = (image_widthz - w) / 2
        y = (image_heightz - h) / 2 + 6
        draw.text(
            (x, y), text, font=font, fill="white", stroke_width=0, stroke_fill="white"
        )
        fname2 = "LogoByAnie.png"
        img.save(fname2, "png")
        await tbot.send_file(event.chat_id, fname2, caption="Made By @Aniebotsupports")
        if os.path.exists(fname2):
            os.remove(fname2)
    except Exception as e:
        await event.reply(f"Error Report @Aniebotsupports, {e}")


@register(pattern="^/rlogo ?(.*)")
async def lego(event):
    quew = event.pattern_match.group(1)
    if event.sender_id == OWNER_ID:
        pass
    else:

        if not quew:
            await event.reply("Provide Some Text To Draw!")
            return
        else:
            pass
    await event.reply("Creating your logo...wait!")
    try:
        text = event.pattern_match.group(1)
        img = Image.open("./SaitamaRobot/resources/blackbg.jpg")
        draw = ImageDraw.Draw(img)
        image_widthz, image_heightz = img.size
        strkcolor = ["yellow", "red", "blue", "purple", "white"]
        font = ImageFont.truetype("./SaitamaRobot/resources/Chopsic.otf", 330)
        w, h = draw.textsize(text, font=font)
        h += int(h * 0.21)
        image_width, image_height = img.size
        draw.text(
            ((image_widthz - w) / 2, (image_heightz - h) / 2),
            text,
            font=font,
            fill=(255, 255, 255),
        )
        x = (image_widthz - w) / 2
        y = (image_heightz - h) / 2 + 6
        draw.text(
            (x, y),
            text,
            font=font,
            fill="black",
            stroke_width=25,
            stroke_fill=random.choice(strkcolor),
        )
        fname2 = "LogoByAnie.png"
        img.save(fname2, "png")
        await tbot.send_file(event.chat_id, fname2, caption="Made By Aniebotsupports")
        if os.path.exists(fname2):
            os.remove(fname2)
    except Exception as e:
        await event.reply(f"Error Report @Aniebotsupports, {e}")


file_help = os.path.basename(__file__)
file_help = file_help.replace(".py", "")
file_helpo = file_help.replace("_", " ")


__mod_name__ = "Logos"
