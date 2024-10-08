import asyncio
from pyrogram import filters
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import ChatPermissions, InlineKeyboardMarkup, InlineKeyboardButton
from config import OWNER_ID
from AnonXMusic import app  # Ensure app is imported properly

# Mute user command in group
@app.on_message(filters.command(["mute"], prefixes=["/"]))
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
    elif len(message.command) > 1:
        user_input = message.command[1]

        # If input is a user ID (number), fetch the user by ID
        if user_input.isdigit():
            try:
                target_user = await client.get_users(int(user_input))
            except Exception as e:
                await message.reply_text(f"User not found: {str(e)}")
                return
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
        await message.reply_text("You can't make me mute my owner.")
        return

    if bot_permission:
        # Check if the target user is an admin or owner
        member = await client.get_chat_member(chat_id, target_user.id)
        if member.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
            try:
                await client.restrict_chat_member(
                    chat_id, 
                    target_user.id,
                    permissions=ChatPermissions(can_send_messages=False)
                )

                # Send a deep link button to open bot's PM with permission settings
                bot_username = (await client.get_me()).username
                mute_message = f"{target_user.first_name} has been muted successfully by {issuer.first_name}."
                button = InlineKeyboardMarkup(
                    [[InlineKeyboardButton("Permissions", url=f"t.me/{bot_username}?start=permissions_{target_user.id}")]]
                )

                print(f"Generated deep link: t.me/{bot_username}?start=permissions_{target_user.id}")

                await message.reply_text(mute_message, reply_markup=button)

            except Exception as e:
                await message.reply_text(f"Failed to mute the user: {str(e)}")
        else:
            await message.reply_text("You cannot mute an admin or owner.")
    else:
        await message.reply_text("I don't have the permission to mute users.")


# Handle the deep link /start=permissions_<user_id> to show permissions in PM
@app.on_message(filters.command("start") & filters.private)
async def handle_start(client, message):
    if message.text.startswith("/start permissions_"):
        target_user_id = int(message.text.split("_")[1])

        # Debugging message to confirm bot got the correct start command
        await message.reply_text(f"Received permission start for user {target_user_id}")

        permissions_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("Text messages", callback_data=f"toggle_text_{target_user_id}")],
            [InlineKeyboardButton("Photo", callback_data=f"toggle_photo_{target_user_id}")],
            [InlineKeyboardButton("Video", callback_data=f"toggle_video_{target_user_id}")],
            [InlineKeyboardButton("Save", callback_data=f"save_permissions_{target_user_id}")]
        ])

        await message.reply_text(
            f"Permission settings for user ID {target_user_id}. Adjust them below:",
            reply_markup=permissions_keyboard
        )