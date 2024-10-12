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
@app.on_message(filters.command(["promote", "fullpromote"], prefixes=["/", "!", ".",","]))
async def promoteFunc(client, message):
    try:
        if message.reply_to_message:
            user = message.reply_to_message.from_user.id
        elif len(message.command) > 1:
            user = message.text.split(None, 1)[1]
            if not user.startswith("@"):  # Ensure the username is in correct format
                user = "@" + user
        else:
            await message.reply("Invalid command usage.")
            return

        user_data = await client.get_users(user)  # Fetch user details
        umention = user_data.mention  # Mention of the user being promoted
        group_name = message.chat.title  # Get the group name
        promoter_mention = message.from_user.mention  # Mention of the person promoting
    except Exception as e:
        await message.reply(f"Invalid ID or user not found. Error: {e}")
        return

    if not user:
        await message.reply("User not found.")
        return

    # Check if bot has promotion rights
    bot_member = await client.get_chat_member(message.chat.id, client.me.id)
    bot_privileges = bot_member.privileges

    if not bot_privileges or not bot_privileges.can_promote_members:
        await message.reply("I don't have the permission to promote members.")
        return

    # Check if the owner is promoting themselves
    if int(user_data.id) == int(message.from_user.id):
        if message.from_user.id == OWNER_ID:
            # Owner can promote themselves without any restrictions
            pass  # Allow the owner to promote themselves
        else:
            await message.reply("You cannot promote yourself unless you're the owner.")
            return

    # For promoting others, check if the promoter (owner) is an admin
    if int(user_data.id) != int(message.from_user.id) and message.from_user.id == OWNER_ID:
        # Owner is allowed to promote others only if they are an admin in the group
        is_admin = await is_administrator(message.from_user.id, message, client)
        if not is_admin:
            await message.reply("As the owner, you need to be an admin to promote others.")
            return

    # Check if non-owners are trying to promote
    if message.from_user.id != OWNER_ID:
        is_admin = await is_administrator(message.from_user.id, message, client)
        if not is_admin:
            await message.reply("You need to be an admin to promote others.")
            return

    try:
        if message.command[0] == "fullpromote":
            await message.chat.promote_member(
                user_id=user_data.id,
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
            await message.reply(f"</b>⬤ ғᴜʟʟᴩʀᴏᴍᴏᴛɪɴɢ ᴀ ᴜsᴇʀ ɪɴ ➠</b> {group_name}\n\n<b>● ᴘʀᴏᴍᴏᴛᴇᴅ ᴜsᴇʀ ➠</b> {umention}\n<b>● ᴩʀᴏᴍᴏᴛᴇʀ ʙʏ ➠</b> {promoter_mention}")
        else:
            await message.chat.promote_member(
                user_id=user_data.id,
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