
__mod_name__ = "FEDERATION "
__help__ = """
          <b>》** ANIE ** 《<b>
            
Ah, group management. It's all fun and games, until you start getting spammers in, and you need to ban them. Then you need to start banning more, and more, and it gets painful.
But then you have multiple groups, and you don't want these spammers in any of your groups - how can you deal? Do you have to ban them manually, in all your groups?
No more! With federations, you can make a ban in one chat overlap to all your other chats.
You can even appoint federation admins, so that your trustworthiest admins can ban across all the chats that you want to protect.
Commands:
- /newfed <fedname>: Creates a new federation with the given name. Only one federation per user. Max 64 chars name allowed.
- /delfed: Deletes your federation, and any information related to it. Will not unban any banned users.
- /fedtransfer <reply/username/mention/userid>: Transfer your federation to another user.
- /renamefed <newname>: Rename your federation.
- /fedinfo <FedID>: Information about a federation.
- /fedadmins <FedID>: List the admins in a federation.
- /fedsubs <FedID>: List all federations your federation is subscribed to.
- /joinfed <FedID>: Join the current chat to a federation. A chat can only join one federation. Chat owners only.
- /leavefed: Leave the current federation. Only chat owners can do this.
- /fedstat: List all the federations you are banned in.
- /fedstat <user ID>: List all the federations a user has been banned in.
- /fedstat <user ID> <FedID>: Gives information about a user's ban in a federation.
- /chatfed: Information about the federation the current chat is in.
Federation admin commands:
- /fban: Bans a user from the current chat's federation
- /unfban: Unbans a user from the current chat's federation
- /feddemoteme <FedID>: Demote yourself from a fed.
- /myfeds: List all your feds.
Federation owner commands:
- /fpromote: Promote a user to fedadmin in your fed.
- /fdemote: Demote a federation admin in your fed.
- /fednotif <yes/no/on/off>: Whether or not to receive PM notifications of every fed action.
- /subfed <FedId>: Subscribe your federation to another. Users banned in the subscribed fed will also be banned in this one.
- /unsubfed <FedId>: Unsubscribes your federation from another. Bans from the other fed will no longer take effect.
- /fedexport <csv/json>: Displays all users who are victimized at the Federation at this time.
- /fedimport: Import a list of banned users.
- /setfedlog <FedId>: Sets the current chat as the federation log. All federation events will be logged here.
- /unsetfedlog <FedId>: Unset the federation log. Events will no longer be logged.
 """
