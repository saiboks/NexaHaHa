import config
from AnonXMusic import app
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ChatPermissions, CallbackQuery
from pyrogram.enums import ChatMemberStatus

@app.on_message(filters.command("mute") & filters.group)
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
        try:
            target_user = await client.get_users(user_input)
        except Exception as e:
            await message.reply_text(f"User not found: {str(e)}")
            return

    if not target_user:
        await message.reply_text("Please reply to a user or provide a valid username/user ID to mute.")
        return

    bot = await client.get_chat_member(chat_id, client.me.id)
    if not bot.privileges.can_restrict_members:
        await message.reply_text("I don't have the permission to mute users.")
        return

    # Mute the user
    try:
        await client.restrict_chat_member(
            chat_id, 
            target_user.id, 
            permissions=ChatPermissions(can_send_messages=False)
        )
        await message.reply_text(
            f"{target_user.first_name} has been muted successfully.",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Set Permissions", url=f"t.me/{client.me.username}?start=setpermissions_{target_user.id}_{chat_id}")]]
            )
        )
    except Exception as e:
        await message.reply_text(f"Failed to mute the user: {str(e)}")


### Unmute Command:
@app.on_message(filters.command("unmute") & filters.group)
async def unmute_user(client, message):
    chat_id = message.chat.id
    target_user = None
    issuer = message.from_user

    # Ensure the user issuing the command has ban rights
    issuer_member = await client.get_chat_member(chat_id, issuer.id)
    if issuer_member.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER] or not issuer_member.privileges.can_restrict_members:
        await message.reply_text("You don't have permission to unmute users.")
        return

    if message.reply_to_message:
        target_user = message.reply_to_message.from_user
    elif len(message.command) > 1:
        user_input = message.command[1]
        try:
            target_user = await client.get_users(user_input)
        except Exception as e:
            await message.reply_text(f"User not found: {str(e)}")
            return

    if not target_user:
        await message.reply_text("Please reply to a user or provide a valid username/user ID to unmute.")
        return

    bot = await client.get_chat_member(chat_id, client.me.id)
    if not bot.privileges.can_restrict_members:
        await message.reply_text("I don't have the permission to unmute users.")
        return

    try:
        # Unmute the user
        await client.restrict_chat_member(
            chat_id, 
            target_user.id,
            permissions=ChatPermissions(can_send_messages=True)
        )
        await message.reply_text(f"{target_user.first_name} has been unmuted.")
    except Exception as e:
        await message.reply_text(f"Failed to unmute the user: {str(e)}")


### Permission Settings in PM:
@app.on_message(filters.command("start") & filters.private)
async def start_command(client, message):
    if message.text.startswith("/start setpermissions_"):
        user_id, chat_id = message.text.split("_")[1], message.text.split("_")[2]
        
        # Send permission control buttons
        await message.reply_text(
            "Set permissions for the user:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Text", callback_data=f"perm_text_{user_id}_{chat_id}")],
                [InlineKeyboardButton("Photos", callback_data=f"perm_photo_{user_id}_{chat_id}")],
                [InlineKeyboardButton("Videos", callback_data=f"perm_video_{user_id}_{chat_id}")],
                [InlineKeyboardButton("Save", callback_data=f"save_perms_{user_id}_{chat_id}")]
            ])
        )


### Callback Handler for Permissions:
@app.on_callback_query()
async def handle_callbacks(client, query: CallbackQuery):
    data = query.data
    if data.startswith("perm_"):
        perm_type, user_id, chat_id = data.split("_")[1], data.split("_")[2], data.split("_")[3]

        if perm_type == "text":
            # Toggle text message permission
            await client.restrict_chat_member(
                chat_id, 
                user_id,
                permissions=ChatPermissions(can_send_messages=True)  # Modify as per requirement
            )
            await query.message.edit_text(f"Text permission updated for user {user_id}.")
        
        # Add similar logic for other permissions like photo, video etc.

    elif data.startswith("save_perms_"):
        user_id, chat_id = data.split("_")[1], data.split("_")[2]
        await query.message.edit_text("Permissions saved successfully!")