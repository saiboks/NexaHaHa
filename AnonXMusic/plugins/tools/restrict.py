import config
from AnonXMusic import app
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ChatPermissions, CallbackQuery
from pyrogram.enums import ChatMemberStatus


# Mute command
@app.on_message(filters.command(["mute"], prefixes=["/", "!", ".",","]))
async def mute_user(client, message):
    chat_id = message.chat.id
    target_user = None
    issuer = message.from_user  # The user issuing the mute command

    # Ensure the user issuing the command has ban rights
    issuer_member = await client.get_chat_member(chat_id, issuer.id)
    if issuer_member.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER] or not issuer_member.privileges.can_restrict_members:
        await message.reply_text("You don't have permission to mute users.")
        return

    # If command is a reply to a message, mute the replied user
    if message.reply_to_message:
        target_user = message.reply_to_message.from_user
    # If user ID or username is provided in the command
    elif len(message.command) > 1:
        user_input = message.command[1]

        # If input is a user ID (number), fetch the user by ID
        if user_input.isdigit():
            try:
                target_user = await client.get_users(int(user_input))
            except Exception as e:
                await message.reply_text(f"User not found: {str(e)}")
                return
        # If input is a username, fetch the user by username
        else:
            try:
                target_user = await client.get_users(user_input)
            except Exception as e:
                await message.reply_text(f"User not found: {str(e)}")
                return

    if not target_user:
        await message.reply_text("Please reply to a user or provide a valid username/user ID to mute.")
        return

    bot = await client.get_chat_member(chat_id, client.me.id)
    bot_permission = bot.privileges.can_restrict_members

    # Check if the target user is the owner
    if target_user.id == OWNER_ID:
        await message.reply_text("You can't make me silence my master.")
        return

    if bot_permission:
        # Check if the target user is an admin or owner
        member = await client.get_chat_member(chat_id, target_user.id)
        if member.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
            try:
                # Mute the user (restrict sending messages)
                await client.restrict_chat_member(
                    chat_id, 
                    target_user.id,
                    permissions=ChatPermissions(can_send_messages=False)
                )
                group_name = message.chat.title if message.chat.title else "this group"
                await message.reply_text(
                    f"{target_user.first_name} has been muted successfully by {issuer.first_name} in {group_name}."
                )
            except Exception as e:
                await message.reply_text(f"Failed to mute the user: {str(e)}")
        else:
            await message.reply_text("You cannot mute an admin or owner.")
    else:
        await message.reply_text("I don't have the permission to mute users.")


# Mute command
@app.on_message(filters.command(["unmute"], prefixes=["/", "!", ".",","]))
async def unmute_user(client, message):
    chat_id = message.chat.id
    target_user = None
    issuer = message.from_user  # The user issuing the unmute command

    # Ensure the user issuing the command has ban rights
    issuer_member = await client.get_chat_member(chat_id, issuer.id)
    if issuer_member.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER] or not issuer_member.privileges.can_restrict_members:
        await message.reply_text("You don't have permission to unmute users.")
        return

    # If command is a reply to a message, unmute the replied user
    if message.reply_to_message:
        target_user = message.reply_to_message.from_user
    # If user ID or username is provided in the command
    elif len(message.command) > 1:
        user_input = message.command[1]

        # If input is a user ID (number), fetch the user by ID
        if user_input.isdigit():
            try:
                target_user = await client.get_users(int(user_input))
            except Exception as e:
                await message.reply_text(f"User not found: {str(e)}")
                return
        # If input is a username, fetch the user by username
        else:
            try:
                target_user = await client.get_users(user_input)
            except Exception as e:
                await message.reply_text(f"User not found: {str(e)}")
                return

    if not target_user:
        await message.reply_text("Please reply to a user or provide a valid username/user ID to unmute.")
        return

    bot = await client.get_chat_member(chat_id, client.me.id)
    bot_permission = bot.privileges.can_restrict_members

    # Remove the check for owner ID to allow unmuting
    if bot_permission:
        # Unmute the user and restore full permissions
        try:
            await client.restrict_chat_member(
                chat_id, 
                target_user.id,
                permissions=ChatPermissions(
                    can_send_messages=True,
                    can_send_media_messages=True,  # This covers media, stickers, GIFs
                    can_send_polls=True,
                    can_add_web_page_previews=True,
                    can_change_info=True,
                    can_invite_users=True,
                    can_pin_messages=True
                )
            )
            group_name = message.chat.title if message.chat.title else "this group"
            await message.reply_text(
                f"{target_user.first_name} has been unmuted successfully by {issuer.first_name} in {group_name}."
            )
        except Exception as e:
            await message.reply_text(f"Failed to unmute the user: {str(e)}")
    else:
        await message.reply_text("I don't have the permission to unmute users.")