import config
from AnonXMusic import app
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ChatPermissions, CallbackQuery
from pyrogram.enums import ChatMemberStatus


# Mute command
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

    # Handle reply or input username/user ID to mute
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

    # Mute the user and send PM with permissions control buttons
    try:
        await client.restrict_chat_member(chat_id, target_user.id, permissions=ChatPermissions(can_send_messages=False))
        await message.reply_text(f"{target_user.first_name} has been muted.")

        # Send buttons to target user's PM
        await client.send_message(
            target_user.id,
            "You've been muted. Please select your permissions:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("✅ Text", callback_data="allow_text"), InlineKeyboardButton("❌ Text", callback_data="deny_text")],
                [InlineKeyboardButton("✅ Photo", callback_data="allow_photo"), InlineKeyboardButton("❌ Photo", callback_data="deny_photo")],
                [InlineKeyboardButton("✅ Video", callback_data="allow_video"), InlineKeyboardButton("❌ Video", callback_data="deny_video")],
                [InlineKeyboardButton("Save", callback_data="save_permissions")]
            ])
        )
    except Exception as e:
        await message.reply_text(f"Failed to mute the user: {str(e)}")

# Handle /start command in PM
@app.on_message(filters.command("start") & filters.private)
async def start_private(client, message):
    await message.reply_text(
        "Welcome to the bot! Please choose your permissions below:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("✅ Text", callback_data="allow_text"), InlineKeyboardButton("❌ Text", callback_data="deny_text")],
            [InlineKeyboardButton("✅ Photo", callback_data="allow_photo"), InlineKeyboardButton("❌ Photo", callback_data="deny_photo")],
            [InlineKeyboardButton("✅ Video", callback_data="allow_video"), InlineKeyboardButton("❌ Video", callback_data="deny_video")],
            [InlineKeyboardButton("Save", callback_data="save_permissions")]
        ])
    )

# Handle button clicks in PM (permissions control)
@app.on_callback_query()
async def handle_callback_query(client, callback_query):
    data = callback_query.data
    user_id = callback_query.from_user.id

    if data.startswith("allow_"):
        await callback_query.answer(f"Permission for {data.split('_')[1]} allowed!")
        # Here you would enable the corresponding permission for the user
    elif data.startswith("deny_"):
        await callback_query.answer(f"Permission for {data.split('_')[1]} denied!")
        # Here you would disable the corresponding permission for the user
    elif data == "save_permissions":
        await callback_query.answer("Permissions saved successfully!")
        await callback_query.message.edit_text("Permissions have been updated.")

if __name__ == "__main__":
    app.run()