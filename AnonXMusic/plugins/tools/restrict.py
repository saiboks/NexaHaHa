from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ChatPermissions  # Corrected import
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import Message
from config import OWNER_ID

# Initialize your bot client
app = Client("my_bot")

# Mute command to mute a user
@app.on_message(filters.command(["mute"], prefixes=["/"]))
async def mute_user(client, message: Message):
    chat_id = message.chat.id
    target_user = None
    issuer = message.from_user  # The user issuing the mute command

    # Ensure the user issuing the command has mute rights
    issuer_member = await client.get_chat_member(chat_id, issuer.id)
    if issuer_member.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER] or not issuer_member.privileges.can_restrict_members:
        await message.reply_text("You don't have permission to mute users.")
        return

    # If command is a reply to a message, mute the replied user
    if message.reply_to_message:
        target_user = message.reply_to_message.from_user
    else:
        await message.reply_text("Please reply to a user to mute.")
        return

    bot = await client.get_chat_member(chat_id, client.me.id)
    if not bot.privileges.can_restrict_members:
        await message.reply_text("I don't have permission to mute users.")
        return

    # Check if the target user is the owner
    if target_user.id == OWNER_ID:
        await message.reply_text("You can't mute the owner.")
        return

    # Mute the user
    await client.restrict_chat_member(
        chat_id,
        target_user.id,
        permissions=ChatPermissions(can_send_messages=False)
    )

    # Bot's username for deep link
    bot_username = (await client.get_me()).username
    deep_link = f"https://t.me/{bot_username}?start=permissions_{target_user.id}"

    # Send mute confirmation with "Permissions" button
    mute_message = f"{target_user.first_name} has been muted successfully."
    button = InlineKeyboardMarkup(
        [[InlineKeyboardButton("Permissions", url=deep_link)]]
    )
    await message.reply_text(mute_message, reply_markup=button)

# Start command in PM
@app.on_message(filters.command("start") & filters.private)
async def start_pm(client, message: Message):
    if len(message.text.split()) > 1:
        command_part = message.text.split(None, 1)[1]
        if command_part.startswith("permissions_"):
            target_user_id = int(command_part.split("_")[1])
            
            # Display permission options
            permissions_keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("Text messages", callback_data=f"toggle_text_{target_user_id}")],
                [InlineKeyboardButton("Photo", callback_data=f"toggle_photo_{target_user_id}")],
                [InlineKeyboardButton("Save", callback_data=f"save_permissions_{target_user_id}")]
            ])

            await message.reply_text(
                f"These are the permission settings for user ID {target_user_id}:",
                reply_markup=permissions_keyboard
            )
        else:
            await message.reply_text("Invalid command.")
    else:
        await message.reply_text("Use a valid command to start.")

# Handle callback queries for permissions
@app.on_callback_query()
async def handle_callbacks(client, callback_query):
    data = callback_query.data

    # Handle toggling permission buttons
    if data.startswith("toggle_"):
        target_user_id = int(data.split("_")[2])
        permission_type = data.split("_")[1]

        # Example: Toggle karne ka message display karna
        await callback_query.answer(f"Toggled {permission_type} for user ID {target_user_id}")

    # Save button handle karna
    elif data.startswith("save_permissions_"):
        target_user_id = int(data.split("_")[1])
        await callback_query.answer(f"Permissions saved for user ID {target_user_id}")

