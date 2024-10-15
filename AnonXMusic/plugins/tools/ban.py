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

    # Agar user ID ya reply nahi mila toh error message dikhaye
    if not user_id:
        command = message.command[0]
        return await message.reply_text(
            f"ᴜsᴇʀ ɴᴏᴛ ғᴏᴜɴᴅ.\nᴛʜᴇ ᴄᴏᴍᴍᴀɴᴅ /{command} ᴍᴜsᴛ ʙᴇ ᴜsᴇᴅ sᴘᴇᴄɪғʏɪɴɢ ᴜsᴇʀ ᴜsᴇʀɴᴀᴍᴇ/ɪᴅ/ᴍᴇɴᴛɪᴏɴ ᴏʀ ʀᴇᴘʟʏɪɴɢ ᴛᴏ ᴏɴᴇ ᴏғ ᴛʜᴇɪʀ ᴍᴇssᴀɢᴇs."
        )

    # Permission check agar user ko allow nahi hai toh custom message show karega
    if not await member_permissions(message):
        command = message.command[0]
        return await message.reply_text(
            f"ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴘᴇʀᴍɪssɪᴏɴ ᴛᴏ ᴜsᴇ ᴀ /{command} ᴏʀᴅᴇʀ."
        )

    # Rest of the ban logic
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
        f"**Banned User:** {mention}\n"
        f"**Banned By:** {message.from_user.mention if message.from_user else 'Anon'}\n"
    )
    
    if reason:
        msg += f"**Reason:** {reason}"
    
    await message.chat.ban_member(user_id)
    replied_message = message.reply_to_message
    if replied_message:
        message = replied_message
    await message.reply_text(msg)


# sban
@app.on_message(
    filters.command(["sban"]) & ~filters.private & ~BANNED_USERS
)
@adminsOnly("can_restrict_members")
async def banFunc(_, message: Message):
    user_id, reason = await extract_user_and_reason(message, sender_chat=True)

    # Agar user ID ya reply nahi mila toh error message dikhaye
    if not user_id:
        command = message.command[0]
        return await message.reply_text(
            f"<b><u>» ᴜsᴇʀ ɴᴏᴛ ғᴏᴜɴᴅ.</u></b>\nᴛʜᴇ ᴄᴏᴍᴍᴀɴᴅ <b>/{command}</b> ᴍᴜsᴛ ʙᴇ ᴜsᴇᴅ sᴘᴇᴄɪғʏɪɴɢ ᴜsᴇʀ <b>ᴜsᴇʀɴᴀᴍᴇ/ɪᴅ/ᴍᴇɴᴛɪᴏɴ</b> ᴏʀ ʀᴇᴘʟʏɪɴɢ ᴛᴏ ᴏɴᴇ ᴏғ ᴛʜᴇɪʀ ᴍᴇssᴀɢᴇs."
        )

    # Permission check ke liye user_id pass karna zaruri hai
    if not await member_permissions(message.from_user.id):
        command = message.command[0]
        return await message.reply_text(
            f"ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴘᴇʀᴍɪssɪᴏɴ ᴛᴏ ᴜsᴇ ᴀ /{command} ᴏʀᴅᴇʀ."
        )

    # Rest of the ban logic
    if user_id == app.id:
        return await message.reply_text("I can't ban myself, I can leave if you want.")
    if user_id in SUDOERS:
        return await message.reply_text("You Wanna Ban The Elevated One? RECONSIDER!")
    if user_id in [
        member.user.id
        async for member in app.get_chat_members(
            chat_id=message.chat.id, filter=ChatMembersFilter.ADMINISTRATORS
        )
    ]:
        return await message.reply_text(
            "I can't ban an admin, You know the rules, so do I."
        )

    try:
        mention = (await app.get_users(user_id)).mention
    except IndexError:
        mention = (
            message.reply_to_message.sender_chat.title
            if message.reply_to_message
            else "Anon"
        )

    # Ban karne wale ka mention remove kar diya gaya hai
    msg = f"**Banned User:** {mention}\n"

    if reason:
        msg += f"**Reason:** {reason}"

    await message.chat.ban_member(user_id)
    
    # Ban command message delete karna
    await message.delete()

    replied_message = message.reply_to_message
    if replied_message:
        message = replied_message
    await message.reply_text(msg)