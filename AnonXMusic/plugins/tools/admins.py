from config import OWNER_ID
from pyrogram import filters, Client
from AnonXMusic import app
from pyrogram.types import ChatPrivileges
from pyrogram.enums import ChatMembersFilter

# Check if user has admin rights
async def is_administrator(user_id: int, message, client):
    admin = False
    administrators = []
    async for m in app.get_chat_members(message.chat.id, filter=ChatMembersFilter.ADMINISTRATORS):
        administrators.append(m)
    for user in administrators:
        if user.user.id == user_id:
            admin = True
            break
    return admin


# Promote function
@app.on_message(filters.command(["promote", "fullpromote"], prefixes=["/", "!", ".", ","]))
async def promoteFunc(client, message):
    try:
        user = None
        if message.reply_to_message:
            user = message.reply_to_message.from_user.id
        elif len(message.command) > 1:
            user = message.text.split(None, 1)[1]
            if not user.startswith("@"):  # Ensure the username is in correct format
                user = "@" + user

        if not user:
            command_name = message.command[0]  # Get the command name
            await message.reply(f"<u><b>ᴜsᴇʀ ɴᴏᴛ ғᴏᴜɴᴅ.</u></b>\nᴛʜᴇ ᴄᴏᴍᴍᴀɴᴅ /{command_name} ᴍᴜsᴛ ʙᴇ ᴜsᴇᴅ sᴘᴇᴄɪғʏɪɴɢ ᴜsᴇʀ <b>ᴜsᴇʀɴᴀᴍᴇ/ɪᴅ/ᴍᴇɴᴛɪᴏɴ ᴏʀ ʀᴇᴘʟʏɪɴɢ</b> ᴛᴏ ᴏɴᴇ ᴏғ ᴛʜᴇɪʀ ᴍᴇssᴀɢᴇs.")
            return

        user_data = await client.get_users(user)  # Fetch user details
        umention = user_data.mention  # Mention of the user being promoted
        group_name = message.chat.title  # Get the group name
        promoter_mention = message.from_user.mention  # Mention of the person promoting
    except Exception as e:
        await message.reply(f"Invalid ID or user not found. Error: {e}")
        return

    # Check if bot has promotion rights
    bot_member = await client.get_chat_member(message.chat.id, client.me.id)
    bot_privileges = bot_member.privileges

    if not bot_privileges or not bot_privileges.can_promote_members:
        await message.reply("I don't have the permission to promote members.")
        return

    # Check if the person issuing the command has promotion rights
    user_member = await client.get_chat_member(message.chat.id, message.from_user.id)
    if not user_member.privileges or not user_member.privileges.can_promote_members:
        await message.reply("You don't have permission to promote members.")
        return

    # Allow only the bot's owner to self-promote
    if int(user_data.id) == int(message.from_user.id) and message.from_user.id != OWNER_ID:
        await message.reply("You cannot promote yourself.")
        return

    try:
        if message.command[0] == "fullpromote":
            await message.chat.promote_member(
                user_id=user_data.id,
                privileges=ChatPrivileges(
                    can_change_info=True,
                    can_invite_users=True,
                    can_delete_messages=True,
                    can_restrict_members=True,
                    can_pin_messages=True,
                    can_promote_members=True,
                    can_manage_chat=True,
                    can_manage_video_chats=True,
                ),
            )
            await message.reply(f"</b>⬤ ғᴜʟʟᴩʀᴏᴍᴏᴛɪɴɢ ᴀ ᴜsᴇʀ ɪɴ ➠</b> {group_name}\n\n<b>● ᴘʀᴏᴍᴏᴛᴇᴅ ᴜsᴇʀ ➠</b> {umention}\n<b>● ᴩʀᴏᴍᴏᴛᴇʀ ʙʏ ➠</b> {promoter_mention}")
        else:
            await message.chat.promote_member(
                user_id=user_data.id,
                privileges=ChatPrivileges(
                    can_change_info=False,
                    can_invite_users=True,
                    can_delete_messages=True,
                    can_restrict_members=False,
                    can_pin_messages=True,
                    can_promote_members=False,
                    can_manage_chat=True,
                    can_manage_video_chats=True,
                ),
            )
            await message.reply(f"<b>⬤ ᴩʀᴏᴍᴏᴛɪɴɢ ᴀ ᴜsᴇʀ ɪɴ ➠</b> {group_name}\n\n<b>● ᴩʀᴏᴍᴏᴛᴇᴅ ᴜsᴇʀ ➠</b> {umention}\n<b>● ᴩʀᴏᴍᴏᴛᴇʀ ʙʏ ➠</b> {promoter_mention}")
    except Exception as err:
        await message.reply(f"An error occurred: {err}")


# Demote function
@app.on_message(filters.command(["demote"], prefixes=["/", "!", ".",","]))
async def demoteFunc(client, message):
    try:
        if message.reply_to_message:
            user = message.reply_to_message.from_user.id
        elif not message.reply_to_message and len(message.command) > 1:
            user = message.text.split(None, 1)[1]
            if not user.startswith("@"):  # Ensure the username is in correct format
                user = "@" + user
        else:
            await message.reply("<u><b>ᴜsᴇʀ ɴᴏᴛ ғᴏᴜɴᴅ.</u></b>\nᴛʜᴇ ᴄᴏᴍᴍᴀɴᴅ /{command_name} ᴍᴜsᴛ ʙᴇ ᴜsᴇᴅ sᴘᴇᴄɪғʏɪɴɢ ᴜsᴇʀ <b>ᴜsᴇʀɴᴀᴍᴇ/ɪᴅ/ᴍᴇɴᴛɪᴏɴ ᴏʀ ʀᴇᴘʟʏɪɴɢ</b> ᴛᴏ ᴏɴᴇ ᴏғ ᴛʜᴇɪʀ ᴍᴇssᴀɢᴇs.")
            return

        user_data = await client.get_users(user)  # Fetch user details
        umention = user_data.mention  # Mention of the user being demoted
        group_name = message.chat.title  # Get the group name
        promoter_mention = message.from_user.mention  # Mention of the person demoting
    except Exception as e:
        await message.reply(f"Invalid ID or user not found. Error: {e}")
        return

    bot_member = await client.get_chat_member(message.chat.id, client.me.id)
    bot_privileges = bot_member.privileges

    if not bot_privileges or not bot_privileges.can_promote_members:
        await message.reply("I don't have the permission to demote members.")
        return

    # Prevent self-demotion unless user is the owner
    if int(user_data.id) == int(message.from_user.id) and message.from_user.id != OWNER_ID:
        await message.reply("You cannot demote yourself unless you're the owner.")
        return

    if not await is_administrator(message.from_user.id, message, client):
        await message.reply("You do not have the permission to demote members.")
        return

    try:
        await message.chat.promote_member(
            user_id=user_data.id,
            privileges=ChatPrivileges(
                can_change_info=False,
                can_invite_users=False,
                can_delete_messages=False,
                can_restrict_members=False,
                can_pin_messages=False,
                can_promote_members=False,
                can_manage_chat=False,
                can_manage_video_chats=False,
            )
        )
        await message.reply(f"<b>⬤ sᴜᴄᴄᴇssғᴜʟʟʏ ᴅᴇᴍᴏᴛᴇᴅ ᴀ ᴀᴅᴍɪɴ ɪɴ ➠</b> {group_name}\n\n<b>● ᴅᴇᴍᴏᴛᴇᴅ ᴜsᴇʀ ➠</b> {umention}\n● ᴩʀᴏᴍᴏᴛᴇʀ ʙʏ ➠</b> {promoter_mention}")
    except Exception as err:
        await message.reply(f"Error: {err}")