import asyncio
from pyrogram import filters
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from AnonXMusic import app
from AnonXMusic.misc import SUDOERS
from config import BANNED_USERS

# kickall with approve/decline buttons, restricted to bot owner or group owner
@app.on_message(filters.command("kickall") & ~filters.private & ~BANNED_USERS)
async def kick_all_func(_, message: Message):
    user_id = message.from_user.id

    # Check if the user is the bot owner or the group owner
    chat_member = await app.get_chat_member(message.chat.id, user_id)
    if user_id not in SUDOERS and chat_member.status != ChatMemberStatus.OWNER:
        return await message.reply_text("ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴛᴏ ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ. ᴏɴʟʏ ᴛʜᴇ ɢʀᴏᴜᴘ ᴏᴡɴᴇʀ ᴄᴀɴ ᴜsᴇ ᴛʜɪs.")

    # Create inline keyboard for approval
    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("ᴀᴘᴘʀᴏᴠᴇ", callback_data="approve_kickall"),
                InlineKeyboardButton("ᴅᴇᴄʟɪɴᴇ", callback_data="decline_kickall")
            ]
        ]
    )
    
    # Send confirmation message with buttons
    await message.reply_text(
        "⚠️ ᴀʀᴇ ʏᴏᴜ sᴜʀᴇ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴋɪᴄᴋ ᴀʟʟ ᴍᴇᴍʙᴇʀs ғʀᴏᴍ ᴛʜɪs ᴄʜᴀᴛ?",
        reply_markup=buttons
    )

# Callback query handler for approve/decline
@app.on_callback_query(filters.regex("^(approve_kickall|decline_kickall)$"))
async def handle_kickall_confirmation(client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    chat_member = await client.get_chat_member(callback_query.message.chat.id, user_id)

    # Check if the user is the bot owner or the group owner
    if user_id not in SUDOERS and chat_member.status != ChatMemberStatus.OWNER:
        await callback_query.answer("❌ ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴛᴏ ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ. ᴏɴʟʏ ᴛʜᴇ ɢʀᴏᴜᴘ ᴏᴡɴᴇʀ ᴄᴀɴ ᴜsᴇ ᴛʜɪs.", show_alert=True)
        return

    if callback_query.data == "approve_kickall":
        await callback_query.message.edit_text("<b>ᴋɪᴄᴋɪɴɢ ᴀʟʟ ᴍᴇᴍʙᴇʀs . . .</b>")
        kicked_count = 0
        failed_count = 0

        async for member in app.get_chat_members(callback_query.message.chat.id):
            user_id = member.user.id
            # Skip if user is the bot itself, an admin, or a SUDOER
            if user_id == app.id or user_id in SUDOERS or member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
                continue
            
            try:
                await callback_query.message.chat.ban_member(user_id)
                await asyncio.sleep(0.5)  # Add small delay to avoid flood limits
                await callback_query.message.chat.unban_member(user_id)
                kicked_count += 1
            except Exception:
                failed_count += 1

        await callback_query.message.edit_text(
            f"<b>sᴜᴄᴄᴇssғᴜʟʟʏ ᴋɪᴄᴋᴇᴅ <u>{kicked_count}</u> ᴜsᴇʀs\nғᴀɪʟᴇᴅ ᴛᴏ ᴋɪᴄᴋ <u>{failed_count}</u> ᴜsᴇʀs</b>"
        )
    elif callback_query.data == "decline_kickall":
        await callback_query.message.edit_text("<b>ᴋɪᴄᴋᴀʟʟ ᴏᴘᴇʀᴀᴛɪᴏɴ ᴄᴀɴᴄᴇʟʟᴇᴅ . . .</b>")