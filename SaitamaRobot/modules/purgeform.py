
from pyrogram import Client, filters
from SaitamaRobot.modules.pyrogram import member_permissions 

def PurgeDictDataUpdater(chat_id, purge_from=None, purge_to=None, first_messageID=None, purge_from_messageID=None):
    PurgeData = PurgeDictData.PurgeDict
    if purge_to == None:
        PurgeData.update(
            {
                chat_id: {
                    "purge_from": purge_from,
                    "first_messageID": first_messageID,
                    "purge_from_messageID": purge_from_messageID
                }
            }
        )
    elif purge_from == None:
        PurgeData[chat_id].update(
            {
                "purge_to": purge_to
            }
        )
    
    

class PurgeDictData:
    PurgeDict = dict()
      
from SaitamaRobot import pbot as StellaCli

from tg_bot import pbot
@pbot.on_message(
    filters.command(['purgefrom', 'purgeto']))
async def PurgeBetween(client, message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    message_id = message.message_id 
    command = message.command[0]
    MessagesIDs = []
    PurgeData = PurgeDictData.PurgeDict

    permissions = await member_permissions(chat_id, user_id)
    if "can_pin_messages" not in permissions:
         await m.reply_text("You Don't Have Enough Permissions.")
         return     

    if not message.reply_to_message:
        await message.reply(
            'Reply to a message to show me where to purge from.'
        )
        return
        
    reply_to_message = message.reply_to_message.message_id
    if command == 'purgefrom':
        purge_from_message = await message.reply(
            "Message marked for deletion. Reply to another message with /purgeto to delete all messages in between."
        )
        purge_from_messageID = purge_from_message.message_id
        PurgeDictDataUpdater(
            chat_id, purge_from=reply_to_message,
            first_messageID=message_id,
            purge_from_messageID=purge_from_messageID
            )
        return

    elif command == 'purgeto':

        if not message.reply_to_message:
            await message.reply(
                'Reply to a message to let me know what to delete.'
            )
            return

        if chat_id in PurgeData.keys():
            PurgeDictDataUpdater(chat_id, purge_to=(reply_to_message + 1))

            purge_from = PurgeData[chat_id]['purge_from']
            first_messageID = PurgeData[chat_id]['first_messageID']
            purge_from_messageID = PurgeData[chat_id]['purge_from_messageID']
            purge_to = PurgeData[chat_id]['purge_to']

            ExtraMessageIDs = [
                message_id,
                first_messageID,
                purge_from_messageID
            ]

            for MessageID in range(purge_from, purge_to):
                MessagesIDs.append(MessageID)
            
            for MessageID in ExtraMessageIDs:
                MessagesIDs.append(MessageID)
            
            try:
                await StellaCli.delete_messages(
                    chat_id=chat_id,
                    message_ids=MessagesIDs
                )
                PurgeData.clear()
            except:
                await message.reply(
                    "I can't delete messages here! Make sure I'm admin and can delete other user's messages."
                )
            await message.reply(
                "Purge completed!"
            )
        else:
            await message.reply(
                "You can only use this command after having used the /purgefrom command."
            )




