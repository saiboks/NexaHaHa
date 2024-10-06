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
@app.on_message(filters.command(["promote", "fullpromote"], "."))
async def promoteFunc(client, message):
    try:
        if message.reply_to_message:
            user = message.reply_to_message.from_user.id
        elif len(message.command) > 1:
            user = message.text.split(None, 1)[1]
        else:
            await message.reply("Invalid command usage.")
            return

        user_data = await client.get_users(user)  # Fetch user details
        umention = user_data.mention  # Mention of the user being promoted
        group_name = message.chat.title  # Get the group name
        promoter_mention = message.from_user.mention  # Mention of the person promoting
    except Exception:
        await message.reply("Invalid ID or user not found.")
        return

    if not user:
        await message.reply("User not found.")
        return

    bot_member = await client.get_chat_member(message.chat.id, client.me.id)
    bot_privileges = bot_member.privileges

    if not bot_privileges or not bot_privileges.can_promote_members:
        await message.reply("I don't have the permission to promote members.")
        return

    if user == message.from_user.id and message.from_user.id != OWNER_ID:
        await message.reply("You cannot promote yourself unless you're the owner.")
        return

    try:
        if message.command[0] == "fullpromote":
            await message.chat.promote_member(
                user_id=user,
                privileges=ChatPrivileges(
                    can_change_info=bot_privileges.can_change_info,
                    can_invite_users=bot_privileges.can_invite_users,
                    can_delete_messages=bot_privileges.can_delete_messages,
                    can_restrict_members=bot_privileges.can_restrict_members,
                    can_pin_messages=bot_privileges.can_pin_messages,
                    can_promote_members=bot_privileges.can_promote_members,
                    can_manage_chat=bot_privileges.can_manage_chat,
                    can_manage_video_chats=bot_privileges.can_manage_video_chats,
                ),
            )
            await message.reply(f"⬤ ғᴜʟʟᴩʀᴏᴍᴏᴛɪɴɢ ᴀ ᴜsᴇʀ ɪɴ ➠ {group_name}\n\n● ᴘʀᴏᴍᴏᴛᴇᴅ ᴜsᴇʀ ➠ {umention}\n● ᴩʀᴏᴍᴏᴛᴇʀ ʙʏ ➠ {promoter_mention}")
        else:
            await message.chat.promote_member(
                user_id=user,
                privileges=ChatPrivileges(
                    can_change_info=False,
                    can_invite_users=bot_privileges.can_invite_users,
                    can_delete_messages=bot_privileges.can_delete_messages,
                    can_restrict_members=False,
                    can_pin_messages=bot_privileges.can_pin_messages,
                    can_promote_members=False,
                    can_manage_chat=bot_privileges.can_manage_chat,
                    can_manage_video_chats=bot_privileges.can_manage_video_chats,
                ),
            )
            await message.reply(f"{umention} has been promoted in {group_name} by {promoter_mention}.")
    except Exception as err:
        await message.reply(f"An error occurred: {err}")

# Demote function
@app.on_message(filters.command(["demote"], "."))
async def demoteFunc(client, message):
    try:
        if message.reply_to_message:
            user = message.reply_to_message.from_user.id
        elif not message.reply_to_message and len(message.command) > 1:
            user = message.text.split(None, 1)[1]
        else:
            await message.reply("Invalid command usage.")
            return

        user_data = await client.get_users(user)  # Fetch user details
        umention = user_data.mention  # Mention of the user being demoted
        group_name = message.chat.title  # Get the group name
        promoter_mention = message.from_user.mention  # Mention of the person demoting
    except Exception:
        await message.reply("Invalid ID")
        return

    bot_member = await client.get_chat_member(message.chat.id, client.me.id)
    bot_privileges = bot_member.privileges

    if not bot_privileges or not bot_privileges.can_promote_members:
        await message.reply("I don't have the permission to demote members.")
        return

    if user == message.from_user.id and message.from_user.id != OWNER_ID:
        await message.reply("You cannot demote yourself unless you're the owner.")
        return

    if not await is_administrator(message.from_user.id, message, client):
        await message.reply("You do not have the permission to demote members.")
        return

    try:
        await message.chat.promote_member(
            user_id=user,
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
        await message.reply(f"{umention} has been demoted in {group_name} by {promoter_mention}.")
    except Exception as err:
        await message.reply(f"Error: {err}")