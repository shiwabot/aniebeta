# COPYRIGHT (C) 2021 BY LEGENDX22 AND PROBOYX

"""
(((((((((((((((((((((((@LEGENDX22)))))))))))))))))))))))))))
(((((((((((((((((((((((@LEGENDX22)))))))))))))))))))))))))))
(((((((((((((((((((((((@LEGENDX22)))))))))))))))))))))))))))
(((((((((((((((((((((((@LEGENDX22)))))))))))))))))))))))))))
                 MADE BY LEGENDX22 AND PROBOYX
                   CREDITS #TEAMLEGEND 
                PLEASE DON'T REMOVE CREDITS
"""


from telethon import events, Button, custom
import re, os
from userbot import bot
from userbot import Anietelethon
PHOTO = "https://telegra.ph/file/fe58623891803d36979f7.jpg"
@bot.on(events.InlineQuery(pattern="alive"))
async def awake(event):
  builder = event.builder
  aniex = event.sender.first_name
  DENVIL_PRO =  "**Aniebot Status**/n/n"
  DENVIL_PRO += "**ALL System ok**\n/n"
  DENVIL_PRO += "**➬ Telethon:**{Anietelethon}/n/n"
  DENVIL_PRO += "**MY Master** {aniex} ☺️/n/n"
  DENVIL_PRO += "**Full upgrade:**/n/n"
  DENVIL_PRO += "**Aniebot** {Anieversion}\n\n"
  DENVIL_PRO += "**thanks for using me**/n/n"
  BUTTON = [[Button.url("MASTER", "https://t.me/denvil_pro"), Button.url("DEVLOPER", "https://t.me/Denvil_pro")]]
  BUTTON += [[custom.Button.inline("REPOSITORYS", data="DENVIL_PRO")]]
  result = builder.photo(
                    PHOTO,
                    text=DENVIL_PRO,
                    buttons=BUTTON,
                    link_preview=False
                )
  await event.answer([result])




@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"DENVIL_PRO")))
async def callback_query_handler(event):
# inline by  LEGENDX22 And DENVIL🔥
  PROBOYX +=[[Button.url("REPO-ANIE", "https://github.com/ANIETEAM/Aniebots"), Button.url("REPO-GROUP BOT", "https://github.com/Anieteam/AnieRobot")]]
  PROBOYX +=[[Button.url("DEPLOY-ANIE", "https://dashboard.heroku.com/new?button-url=https%3A%2F%2Fgithub.com%2FAnieteam%2FAniebots&template=https%3A%2F%2Fgithub.com%2FAnietEAM%2FAniebots%2FLE"), Button.url("DEPLOY-ANIE GROUP BOT", "https://dashboard.heroku.com/new?button-url=https%3A%2F%2Fgithub.com%2ANIETEAM%2FANIEROBOT&template=https%3A%2F%2Fgithub.com%2FANIETEAM%2FANIEROBOT")]]
  PROBOYX +=[[Button.url("TUTORIAL", "https://youtu.be/T9ojWwGYBtw"), Button.url("STRING-SESSION", "https://repl.it/@denvilop/Aniebots#main.py")]]
  PROBOYX +=[[Button.url("API_ID & HASH", "https://t.me/usetgxbot"), Button.url("REDIS", "https://redislabs.com")]]
  PROBOYX +=[[Button.url("SUPPORT CHANNEL", "https://t.me/ANIEBOTS"), Button.url("SUPPORT GROUP", "https://t.me/Aniebotsupports")]]
  PROBOYX +=[[custom.Button.inline("ALIVE", data="PROBOY")]]
  await event.edit(text=f"ALL DETAILS OF REPOS", buttons=PROBOYX)
