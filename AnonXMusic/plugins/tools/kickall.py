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

# kickall
@app.on_message(filters.command("kickall") & ~filters.private & ~BANNED_USERS)
@adminsOnly("can_restrict_members")
async def kick_all_func(_, message: Message):
    kicked_count = 0
    failed_count = 0

    async for member in app.get_chat_members(message.chat.id):
        user_id = member.user.id
        # Skip if user is the bot itself, an admin, or a SUDOER
        if user_id == app.id or user_id in SUDOERS or member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
            continue
        
        try:
            mention = (await app.get_users(user_id)).mention
            await message.chat.ban_member(user_id)
            await asyncio.sleep(0.5)  # Add small delay to avoid flood limits
            await message.chat.unban_member(user_id)
            kicked_count += 1
        except Exception:
            failed_count += 1

    await message.reply_text(f"✅ Successfully kicked {kicked_count} users.\n❌ Failed to kick {failed_count} users.")