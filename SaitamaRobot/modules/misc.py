import html
from SaitamaRobot.modules.helper_funcs.chat_status import user_admin, dev_plus, sudo_plus, asse_plus
from SaitamaRobot.modules.disable import DisableAbleCommandHandler
from SaitamaRobot import dispatcher

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import MessageEntity, ParseMode, Update
from telegram.ext.dispatcher import run_async
from telegram.ext import CallbackContext, Filters, CommandHandler

MARKDOWN_HELP = f"""
Markdown is a very powerful formatting tool supported by telegram. {dispatcher.bot.first_name} has some enhancements, to make sure that \
saved messages are correctly parsed, and to allow you to create buttons.

• <code>_italic_</code>: wrapping text with '_' will produce italic text
• <code>*bold*</code>: wrapping text with '*' will produce bold text
• <code>`code`</code>: wrapping text with '`' will produce monospaced text, also known as 'code'
• <code>[sometext](someURL)</code>: this will create a link - the message will just show <code>sometext</code>, \
and tapping on it will open the page at <code>someURL</code>.
<b>Example:</b><code>[test](example.com)</code>

• <code>[buttontext](buttonurl:someURL)</code>: this is a special enhancement to allow users to have telegram \
buttons in their markdown. <code>buttontext</code> will be what is displayed on the button, and <code>someurl</code> \
will be the url which is opened.
<b>Example:</b> <code>[This is a button](buttonurl:example.com)</code>

If you want multiple buttons on the same line, use :same, as such:
<code>[one](buttonurl://example.com)
[two](buttonurl://google.com:same)</code>
This will create two buttons on a single line, instead of one button per line.

Keep in mind that your message <b>MUST</b> contain some text other than just a button!
"""


@run_async
@sudo_plus
def echo(update: Update, context: CallbackContext):
    args = update.effective_message.text.split(None, 1)
    message = update.effective_message

    if message.reply_to_message:
        message.reply_to_message.reply_text(
            args[1], parse_mode="MARKDOWN", disable_web_page_preview=True)
    else:
        message.reply_text(
            args[1],
            quote=False,
            parse_mode="MARKDOWN",
            disable_web_page_preview=True)
    message.delete()


def markdown_help_sender(update: Update):
    update.effective_message.reply_text(
        MARKDOWN_HELP, parse_mode=ParseMode.HTML)
    update.effective_message.reply_text(
        "Try forwarding the following message to me, and you'll see, and Use #test!"
    )
    update.effective_message.reply_text(
        "/save test This is a markdown test. _italics_, *bold*, code, "
        "[URL](example.com) [button](buttonurl:github.com) "
        "[button2](buttonurl://google.com:same)")


@run_async
def markdown_help(update: Update, context: CallbackContext):
    if update.effective_chat.type != "private":
        update.effective_message.reply_text(
            'Contact me in pm',
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton(
                    "Markdown help",
                    url=f"t.me/{context.bot.username}?start=markdownhelp")
            ]]))
        return
    markdown_help_sender(update)


@run_async
def blacklistst(update: Update, context):
    update.effective_message.reply_text(
        """*Examples:*
- Blacklist sticker is used to stop certain stickers. Whenever a sticker is sent, the message will be deleted immediately.
*NOTE:* Blacklist stickers do not affect the group admin.
 • `/blsticker`*:* See current blacklisted sticker.
*Only admin:*
 • `/addblsticker <sticker link>`*:* Add the sticker trigger to the black list. Can be added via reply sticker.
 • `/unblsticker <sticker link>`*:* Remove triggers from blacklist. The same newline logic applies here, so you can delete multiple triggers at once.
 • `/rmblsticker <sticker link>`*:* Same as above.
 • `/blstickermode <ban/tban/mute/tmute>`*:* sets up a default action on what to do if users use blacklisted stickers. (`tmute seems broken right now`)
Note:
 • `<sticker link>` can be `https://t.me/addstickers/<sticker>` or just `<sticker>` or reply to the sticker message.
""",
        parse_mode=ParseMode.MARKDOWN)

@run_async
def funhelp(update: Update, context):
    update.effective_message.reply_text(
        """*Examples:*
• `/runs`*:* reply a random string from an array of replies
 • `/slap`*:* slap a user, or get slapped if not a reply
 • `/shrug`*:* get shrug XD
 • `/table`*:* get flip/unflip :v
 • `/decide`*:* Randomly answers yes/no/maybe
 • `/toss`*:* Tosses A coin
 • `/bluetext`*:* check urself :V
 • `/roll`*:* Roll a dice
 • `/rlg`*:* Join ears,nose,mouth and create an emo ;-;
 • `/shout <keyword>`*:* write anything you want to give loud shout
 • `/weebify <text>`*:* returns a weebified text
 • `/sanitize`*:* always use this before /pat or any contact
 • `/pat`*:* pats a user, or get patted""",
        parse_mode=ParseMode.MARKDOWN)

def cleanerhelp(update: Update, context):
    update.effective_message.reply_text(
        """*Examples:*
-Blue text cleaner removed any made up commands that people send in your chat.
 • `/cleanblue <on/off/yes/no>`*:* clean commands after sending
 • `/ignoreblue <word>`*:* prevent auto cleaning of the command
 • `/unignoreblue <word>`*:* remove prevent auto cleaning of the command
 • `/listblue`*:* list currently whitelisted commands
 
 *Following are Disasters only commands, admins cannot use these:*
 • `/gignoreblue <word>`*:* globally ignorea bluetext cleaning of saved word across Saitama.
 • `/ungignoreblue <word>`*:* remove said command from global cleaning list""",
        parse_mode=ParseMode.MARKDOWN)

def disasterhelp(update: Update, context):
    update.effective_message.reply_text(
        """*Examples:*
*⚠️ Notice:*
Commands listed here only work for users with special access are mainly used for troubleshooting, debugging purposes.
Group admins/group owners do not need these commands. 

 ╔ *List all special users:*
 ╠ `/dragons`*:* Lists all Dragon disasters
 ╠ `/demons`*:* Lists all Demon disasters
 ╠ `/tigers`*:* Lists all Tigers disasters
 ╠ `/wolves`*:* Lists all Wolf disasters
 ╚ `/heroes`*:* Lists all Hero Association members

 ╔ *Ping:*
 ╠ `/ping`*:* gets ping time of bot to telegram server
 ╚ `/pingall`*:* gets all listed ping times

 ╔ *Broadcast: (Bot owner only)*
 ╠  *Note:* This supports basic markdown
 ╠ `/broadcastall`*:* Broadcasts everywhere
 ╠ `/broadcastusers`*:* Broadcasts too all users
 ╚ `/broadcastgroups`*:* Broadcasts too all groups

 ╔ *Getchats:*
 ╚ `/getchats ID`*:* Gets a list of group names the user has been seen in. Bot owner only

 ╔ *Blacklist:* 
 ╠ `/ignore`*:* Blacklists a user from 
 ╠  using the bot entirely
 ╚ `/notice`*:* Whitelists the user to allow bot usage

 ╔ *Speedtest:*
 ╚ `/speedtest`*:* Runs a speedtest and gives you 2 options to choose from, text or image output

 ╔ *Global Bans:*
 ╠ `/gban user reason`*:* Globally bans a user
 ╚ `/ungban user reason`*:* Unbans the user from the global bans list

 ╔ *Module loading:*
 ╠ `/listmodules`*:* Lists names of all modules
 ╠ `/load modulename`*:* Loads the said module to 
 ╠   memory without restarting.
 ╠ `/unload modulename`*:* Loads the said module from
 ╚   memory without restarting.memory without restarting the bot 

 ╔ *Remote commands:*
 ╠ `/rban user group`*:* Remote ban
 ╠ `/runban user group`*:* Remote un-ban
 ╠ `/rpunch user group`*:* Remote punch
 ╠ `/rmute user group`*:* Remote mute
 ╠ `/runmute user group`*:* Remote un-mute
 ╚ `/ginfo username/link/ID`*:* Pulls info panel for entire group

 ╔ *Windows self hosted only:*
 ╠ `/restart`*:* Restarts the bots service
 ╚ `/gitpull`*:* Pulls the repo and then restarts the bots service

 ╔ *Chatbot:* 
 ╚ `/listaichats`*:* Lists the chats the chatmode is enabled in
 
 ╔ *Debugging and Shell:* 
 ╠ `/debug <on/off>`*:* Logs commands to updates.txt
 ╠ `/eval`*:* Self explanatory
 ╠ `/sh`*:* Self explanator
 ╚ `/py`*:* Self explanatory.""",
        parse_mode=ParseMode.MARKDOWN)

def approvehelp(update: Update, context):
    update.effective_message.reply_text(
         """*Examples:*
*Admin commands:*
- /approval: Check a user's approval status in this chat.
- /approve: Approve of a user. Locks, blacklists, and antiflood won't apply to them anymore.
- /unapprove: Unapprove of a user. They will now be subject to locks, blacklists, and antiflood again.
- /approved: List all approved users.
- /unapproveall unapproved all users """,
           parse_mode=ParseMode.MARKDOWN)

def connecthelp(update: Update, context):
    update.effective_message.reply_text(
         """ example
Sometimes, you just want to add some notes and filters to a group chat, 
but you don't want everyone to see; This is where connections come in...This allows you to connect to a chat's database, 
and add things to it without the commands appearing in chat! 
For obvious reasons, you need to be an admin to add things; 
but any member in the group can view your data. 
• /connect: Connects to chat (Can be done in a group by /connect or /connect <chat id> in PM) 
• /connection: List connected chats 
• /disconnect: Disconnect from a chat 
• /helpconnect: List available commands that can be used remotely*Admin only:* 
• /allowconnect <yes/no>: allow a user to connect to a chat"""
            parse_mode=ParseMode.MARKDOWN)

def blacklisthelp(update: Update, context):
    update.effective_message.reply_text(
          """ example 
Blacklists are used to stop certain triggers from being said in a group. 
Any time the trigger is mentioned, the message will immediately be deleted. 
A good combo is sometimes to pair this up with warn filters!*NOTE* : Blacklists do not affect group admins. 
• `/blacklist`*:* View the current blacklisted words.Admin only: 
• `/addblacklist <triggers>`*:* Add a trigger to the blacklist. Each line is considered one trigger, so using different lines will allow you to add multiple triggers. 
• `/unblacklist <triggers>`*:* Remove triggers from the blacklist. Same newline logic applies here, so you can remove multiple triggers at once. 
• `/blacklistmode <off/del/warn/ban/kick/mute/tban/tmute>`*:* Action to perform when someone sends blacklisted words. 
• `/unblacklistall` Remove All Blacklisted triggers at once [ Chat Owner Only ]"""
                     parse_mode=ParseMode.MARKDOWN)  

def rulshelp(update: Update, context):
    update.effective_message.reply_text(
         """ example 
• `/rules`*:* get the rules for this chat.*Admins only:* 
• `/setrules <your rules here>`*:* set the rules for this chat. 
• `/clearrules`*:* clear the rules for this chat."""
                       parse_mode=ParseMode.MARKDOWN)


__help__ = """
*Available commands:*
*GlobalHandlers*
• `/disasterhelp`*:* *Get Disasters Help*
*BlacklistSticker*
• `/blacklistst`*:* Get BlSticker Help
*blacklisthelp*
•`blacklisthelp`*:* get blacklist help
*ruls*
•`Rulshelp`*:* get ruls help
*Fun*
• `/funhelp`*:* Get Fun Help
*Approve*
•`Approvehelp`*:* get approval help
*Connect*
•`/connecthelp`*:* get connection help
*Cleaner*
• `/cleanerhelp` *:* Get Cleaner Help
*Markdown:*
 • `/markdownhelp`*:* quick summary of how markdown works in telegram - can only be called in private chats
*Paste:*
 • `/paste`*:* Saves replied content to `nekobin.com` and replies with a url
*React:*
 • `/react`*:* Reacts with a random reaction 
*Urban Dictonary:*
 • `/ud <word>`*:* Type the word or expression you want to search use
*Wikipedia:*
 • `/wiki <query>`*:* wikipedia your query
*Currency converter:* 
 • `/cash`*:* currency converter
Example:
 `/cash 1 USD INR`  
      _OR_
 `/cash 1 usd inr`
Output: `1.0 USD = 75.505 INR`
*TIME*
 • `/time <query>`*:* Gives information about a timezone.

*Available queries:* Country Code/Country Name/Timezone Name
• 🕐 [Timezones list](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)
*REVERSE IMAGE*
- `/reverse`: Does a reverse image search of the media which it was replied to.
*TRANSLATER*
• `/tr` or `/tl` (language code) as reply to a long message
*Example:* 
  `/tr en`*:* translates something to english
  `/tr hi-en`*:* translates hindi to english
*STICKERS*
• `/stickerid`*:* reply to a sticker to me to tell you its file ID.
• `/getsticker`*:* reply to a sticker to me to upload its raw PNG file.
• `/kang`*:* reply to a sticker to add it to your pack.
• `/stickers`*:* Find stickers for given term on combot sticker catalogue
"""

ECHO_HANDLER = CommandHandler("echo", echo, filters=Filters.group)
MD_HELP_HANDLER = CommandHandler("markdownhelp", markdown_help)
DISASTERHELP_HANDLER = CommandHandler("disasterhelp", disasterhelp)
BLACKLISTST_HANDLER = CommandHandler("blacklistst", blacklistst)
FUNHELP_HANDLER = CommandHandler("funhelp", funhelp)
CLEANERHELP_HANDLER = CommandHandler("cleanerhelp", cleanerhelp)

dispatcher.add_handler(ECHO_HANDLER)
dispatcher.add_handler(MD_HELP_HANDLER)
dispatcher.add_handler(DISASTERHELP_HANDLER)
dispatcher.add_handler(BLACKLISTST_HANDLER)
dispatcher.add_handler(FUNHELP_HANDLER)
dispatcher.add_handler(CLEANERHELP_HANDLER)

__mod_name__ = "Anie•Extras"
__command_list__ = ["id", "echo"]
__handlers__ = [
    ECHO_HANDLER,
    MD_HELP_HANDLER,
]
