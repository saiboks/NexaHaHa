import asyncio
from time import time
import os
import sys
from pyrogram import Client, enums
from pyrogram import filters
from pyrogram.errors import ChatAdminRequired
from pyrogram.types import ChatPermissions, ChatPrivileges, Message
from AnonXMusic import app
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ChatType, ChatMemberStatus
from pyrogram.errors import (
    ChatAdminRequired,
    InviteRequestSent,
    UserAlreadyParticipant,
    UserNotParticipant,
)
from pyrogram.errors import MessageDeleteForbidden, RPCError
from config import OWNER_ID

@app.on_message(filters.command(["banall"], prefixes=["/"]))
async def banall_command(client, message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    # Get the status of the user in the group (owner or not)
    chat_member = await client.get_chat_member(chat_id, user_id)

    # Check if the user is either the bot owner or the group owner
    if user_id == OWNER_ID or chat_member.status == enums.ChatMemberStatus.OWNER:
        await message.reply_text("ʙᴀɴᴀʟʟ ꜱᴛᴀʀᴛɪɴɢ ...")
        
        bot = await client.get_chat_member(chat_id, client.me.id)
        bot_permission = bot.privileges.can_restrict_members

        if bot_permission:
            async for member in client.get_chat_members(chat_id):
                try:
                    await client.ban_chat_member(chat_id, member.user.id)
                except Exception:
                    pass
        else:
            await message.reply_text("I don't have the right to restrict users or you are not in sudo users.")
    else:
        await message.reply_text("ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴛᴏ ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ. ᴏɴʟʏ ᴛʜᴇ ɢʀᴏᴜᴘ ᴏᴡɴᴇʀ ᴄᴀɴ ᴜsᴇ ᴛʜɪs.")