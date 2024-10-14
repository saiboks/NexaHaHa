import asyncio
from contextlib import suppress

from pyrogram import filters
from pyrogram.enums import ChatMembersFilter, ChatMemberStatus, ChatType
from pyrogram.types import (
    CallbackQuery,
    ChatPermissions,
    ChatPrivileges,
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from string import ascii_lowercase
from typing import Dict, Union

from AnonXMusic import app
from AnonXMusic.misc import SUDOERS
from AnonXMusic.core.mongo import mongodb
from AnonXMusic.utils.error import capture_err
from AnonXMusic.utils.keyboard import ikb
from AnonXMusic.utils.database import save_filter
from AnonXMusic.utils.functions import (
    extract_user,
    extract_user_and_reason,
    time_converter,
)
from AnonXMusic.utils.permissions import adminsOnly, member_permissions
from config import BANNED_USERS

warnsdb = mongodb.warns

# kickall with approve/decline buttons
@app.on_message(filters.command("kickall") & ~filters.private & ~BANNED_USERS)
@adminsOnly("can_restrict_members")
async def kick_all_func(_, message: Message):
    # Create inline keyboard for approval
    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("✅ Approve", callback_data="approve_kickall"),
                InlineKeyboardButton("❌ Decline", callback_data="decline_kickall")
            ]
        ]
    )
    
    # Send confirmation message with buttons
    await message.reply_text(
        "⚠️ Are you sure you want to kick all members from this chat?",
        reply_markup=buttons
    )

# Callback query handler for approve/decline
@app.on_callback_query(filters.regex("^(approve_kickall|decline_kickall)$"))
async def handle_kickall_confirmation(client, callback_query: CallbackQuery):
    # Only allow admins or SUDOERS to approve/decline the action
    user_id = callback_query.from_user.id
    chat_member = await client.get_chat_member(callback_query.message.chat.id, user_id)

    if user_id not in SUDOERS and chat_member.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
        await callback_query.answer("❌ You are not authorized to perform this action.", show_alert=True)
        return

    if callback_query.data == "approve_kickall":
        await callback_query.message.edit_text("✅ Kicking all members...")
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
            f"✅ Successfully kicked {kicked_count} users.\n❌ Failed to kick {failed_count} users."
        )
    elif callback_query.data == "decline_kickall":
        await callback_query.message.edit_text("❌ Kickall operation cancelled.")