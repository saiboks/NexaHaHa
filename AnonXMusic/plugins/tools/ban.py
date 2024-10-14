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

# kick
@app.on_message(filters.command(["kick", "skick"]) & ~filters.private & ~BANNED_USERS)
@adminsOnly("can_restrict_members")
async def kickFunc(_, message: Message):
    user_id, reason = await extract_user_and_reason(message)
    if not user_id:
        return await message.reply_text("I can't find that user.")
    if user_id == app.id:
        return await message.reply_text("I can't kick myself, but I can leave if you want.")
    if user_id in SUDOERS:
        return await message.reply_text("You wanna kick an elevated one?")
    if user_id in [
        member.user.id
        async for member in app.get_chat_members(
            chat_id=message.chat.id, filter=ChatMembersFilter.ADMINISTRATORS
        )
    ]:
        return await message.reply_text("I can't kick an admin.")
    
    # Kick message
    mention = (await app.get_users(user_id)).mention
    msg = f"""
<b>Kicked by:</b> {message.from_user.mention if message.from_user else 'Anonymous'}
<b>Reason:</b> {reason or 'No reason provided'}"""
    
    await message.chat.ban_member(user_id)
    
    # Check for silent kick 'skick'
    if message.command[0][0] == "s":
        if message.reply_to_message:  # Ensure reply_to_message exists before trying to delete it
            await message.reply_to_message.delete()
        await app.delete_user_history(message.chat.id, user_id)  # Delete user history
        await message.delete()  # Delete the command message as well
    else:
        # Send kick message for 'kick' command
        await message.reply_text(msg)
    
    # Unban the user after a short delay
    await asyncio.sleep(1)
    await message.chat.unban_member(user_id)