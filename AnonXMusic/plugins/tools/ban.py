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


# ban
@app.on_message(
    filters.command(["ban"]) & ~filters.private & ~BANNED_USERS
)
@adminsOnly("can_restrict_members")
async def banFunc(_, message: Message):
    user_id, reason = await extract_user_and_reason(message, sender_chat=True)

    if not user_id:
        return await message.reply_text(
            "ᴜsᴇʀ ɴᴏᴛ ғᴏᴜɴᴅ.\n"
            "ᴛʜᴇ ᴄᴏᴍᴍᴀɴᴅ /ban ᴍᴜsᴛ ʙᴇ ᴜsᴇᴅ sᴘᴇᴄɪғʏɪɴɢ ᴜsᴇʀ ᴜsᴇʀɴᴀᴍᴇ/ɪᴅ/ᴍᴇɴᴛɪᴏɴ ᴏʀ ʀᴇᴘʟʏɪɴɢ ᴛᴏ ᴏɴᴇ ᴏғ ᴛʜᴇɪʀ ᴍᴇssᴀɢᴇs."
        )
    if user_id == app.id:
        return await message.reply_text("I can't ban myself, i can leave if you want.")
    if user_id in SUDOERS:
        return await message.reply_text("You Wanna Ban The Elevated One?, RECONSIDER!")
    if user_id in [
        member.user.id
        async for member in app.get_chat_members(
            chat_id=message.chat.id, filter=ChatMembersFilter.ADMINISTRATORS
        )
    ]:
        return await message.reply_text(
            "I can't ban an admin, You know the rules, so do i."
        )

    try:
        mention = (await app.get_users(user_id)).mention
    except IndexError:
        mention = (
            message.reply_to_message.sender_chat.title
            if message.reply_to_message
            else "Anon"
        )

    msg = (
        f"<b>● ʙᴀɴɴᴇᴅ ᴜsᴇʀ ➠</b> {mention}\n"
        f"<b>● ʙᴀɴɴᴇᴅ ʙʏ ➠</b> {message.from_user.mention if message.from_user else 'Anon'}\n"
    )
    if reason:
        msg += f"<b>ʀᴇᴀsᴏɴ ➠</b> {reason}"
    await message.chat.ban_member(user_id)
    replied_message = message.reply_to_message
    if replied_message:
        message = replied_message
    await message.reply_text(msg)